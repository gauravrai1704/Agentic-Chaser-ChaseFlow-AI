"""
API Routes for ChaseFlow AI
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.database import get_db
from app.models import database as db_models
from app.models import schemas
from app.agents.orchestrator import OrchestratorAgent
from app.agents.predictor import PredictorAgent

router = APIRouter()

# Initialize agents
orchestrator = OrchestratorAgent()
predictor = PredictorAgent()


@router.get("/dashboard/stats", response_model=schemas.DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    total_items = db.query(db_models.ChaseItem).count()
    pending_items = db.query(db_models.ChaseItem).filter(
        db_models.ChaseItem.status.in_(["pending", "sent"])
    ).count()
    overdue_items = db.query(db_models.ChaseItem).filter(
        db_models.ChaseItem.status == "overdue"
    ).count()
    
    # Completed today
    today = datetime.utcnow().date()
    completed_today = db.query(db_models.ChaseItem).filter(
        db_models.ChaseItem.status == "received",
        func.date(db_models.ChaseItem.received_date) == today
    ).count()
    
    # Average completion days
    completed_items = db.query(db_models.ChaseItem).filter(
        db_models.ChaseItem.status == "received",
        db_models.ChaseItem.received_date.isnot(None)
    ).all()
    
    if completed_items:
        total_days = sum([
            (item.received_date - item.sent_date).days 
            for item in completed_items 
            if item.sent_date and item.received_date
        ])
        avg_days = total_days / len(completed_items)
    else:
        avg_days = 0.0
    
    # Time saved calculation (assuming 15 min per manual chase)
    total_attempts = db.query(func.sum(db_models.ChaseItem.attempts)).scalar() or 0
    time_saved_hours = (total_attempts * 15) / 60  # 15 minutes per chase
    
    # Automation rate
    total_actions = db.query(db_models.AgentActivity).count()
    successful_actions = db.query(db_models.AgentActivity).filter(
        db_models.AgentActivity.status == "success"
    ).count()
    automation_rate = (successful_actions / total_actions * 100) if total_actions > 0 else 0.0
    
    return schemas.DashboardStats(
        total_chase_items=total_items,
        pending_items=pending_items,
        overdue_items=overdue_items,
        completed_today=completed_today,
        avg_completion_days=round(avg_days, 1),
        time_saved_hours=round(time_saved_hours, 1),
        automation_rate=round(automation_rate, 1),
        active_agents=4  # document_chaser, loa_chaser, predictor, orchestrator
    )


@router.get("/clients", response_model=List[schemas.ClientResponse])
async def get_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all clients"""
    clients = db.query(db_models.Client).offset(skip).limit(limit).all()
    return clients


@router.get("/clients/{client_id}", response_model=schemas.ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    """Get specific client"""
    client = db.query(db_models.Client).filter(db_models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.get("/chase-items", response_model=List[schemas.ChaseItemResponse])
async def get_chase_items(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get chase items with optional filters"""
    query = db.query(db_models.ChaseItem)
    
    if status:
        query = query.filter(db_models.ChaseItem.status == status)
    if priority:
        query = query.filter(db_models.ChaseItem.priority == priority)
    if category:
        query = query.filter(db_models.ChaseItem.category == category)
    
    items = query.order_by(desc(db_models.ChaseItem.created_at)).offset(skip).limit(limit).all()
    return items


@router.get("/chase-items/{item_id}", response_model=schemas.ChaseItemResponse)
async def get_chase_item(item_id: int, db: Session = Depends(get_db)):
    """Get specific chase item"""
    item = db.query(db_models.ChaseItem).filter(db_models.ChaseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Chase item not found")
    return item


@router.post("/chase-items/{item_id}/process")
async def process_chase_item(item_id: int, db: Session = Depends(get_db)):
    """Manually trigger processing of a chase item"""
    item = db.query(db_models.ChaseItem).filter(db_models.ChaseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Chase item not found")
    
    # Convert to dict for processing
    item_dict = {
        "id": item.id,
        "client_id": item.client_id,
        "type": item.type,
        "category": item.category,
        "target": item.target,
        "description": item.description,
        "status": item.status,
        "priority": item.priority,
        "sent_date": item.sent_date,
        "expected_date": item.expected_date,
        "attempts": item.attempts
    }
    
    # Process with orchestrator
    result = await orchestrator.process(item_dict)
    
    # Update database
    item.attempts += 1
    item.last_attempt_date = datetime.utcnow()
    item.updated_at = datetime.utcnow()
    
    # Log activity
    activity = db_models.AgentActivity(
        agent_type=result.get("agent_type", "orchestrator"),
        action=result["action"].get("action", "processed"),
        target=item.target,
        status="success",
        details=str(result),
        chase_item_id=item.id
    )
    db.add(activity)
    db.commit()
    
    return result


@router.get("/predictions/{item_id}", response_model=schemas.PredictionResult)
async def get_prediction(item_id: int, db: Session = Depends(get_db)):
    """Get delay prediction for a chase item"""
    item = db.query(db_models.ChaseItem).filter(db_models.ChaseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Chase item not found")
    
    item_dict = {
        "id": item.id,
        "type": item.type,
        "category": item.category,
        "priority": item.priority,
        "target": item.target,
        "sent_date": item.sent_date,
        "attempts": item.attempts
    }
    
    prediction = await predictor.analyze(item_dict)
    return prediction


@router.get("/activities", response_model=List[schemas.AgentActivityResponse])
async def get_activities(
    limit: int = 50,
    agent_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get recent agent activities"""
    query = db.query(db_models.AgentActivity)
    
    if agent_type:
        query = query.filter(db_models.AgentActivity.agent_type == agent_type)
    
    activities = query.order_by(desc(db_models.AgentActivity.timestamp)).limit(limit).all()
    return activities


@router.get("/communications", response_model=List[schemas.CommunicationResponse])
async def get_communications(
    chase_item_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get communications"""
    query = db.query(db_models.Communication)
    
    if chase_item_id:
        query = query.filter(db_models.Communication.chase_item_id == chase_item_id)
    
    comms = query.order_by(desc(db_models.Communication.sent_at)).limit(limit).all()
    return comms


@router.get("/agents/status")
async def get_agent_statuses():
    """Get status of all agents"""
    statuses = await orchestrator.get_all_agent_statuses()
    return statuses


@router.post("/simulate/activity")
async def simulate_activity():
    """Simulate agent activity for demo"""
    activity = await orchestrator.simulate_activity()
    return activity


@router.get("/analytics/overview")
async def get_analytics_overview(db: Session = Depends(get_db)):
    """Get analytics overview"""
    
    # Chase items by status
    status_counts = db.query(
        db_models.ChaseItem.status,
        func.count(db_models.ChaseItem.id)
    ).group_by(db_models.ChaseItem.status).all()
    
    # Chase items by category
    category_counts = db.query(
        db_models.ChaseItem.category,
        func.count(db_models.ChaseItem.id)
    ).group_by(db_models.ChaseItem.category).all()
    
    # Chase items by priority
    priority_counts = db.query(
        db_models.ChaseItem.priority,
        func.count(db_models.ChaseItem.id)
    ).group_by(db_models.ChaseItem.priority).all()
    
    # Recent activity trend (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_activities = db.query(
        func.date(db_models.AgentActivity.timestamp).label('date'),
        func.count(db_models.AgentActivity.id).label('count')
    ).filter(
        db_models.AgentActivity.timestamp >= seven_days_ago
    ).group_by(func.date(db_models.AgentActivity.timestamp)).all()
    
    return {
        "status_distribution": dict(status_counts),
        "category_distribution": dict(category_counts),
        "priority_distribution": dict(priority_counts),
        "daily_activity_trend": [
            {"date": str(date), "count": count} 
            for date, count in daily_activities
        ]
    }
