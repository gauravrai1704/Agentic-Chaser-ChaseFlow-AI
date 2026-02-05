"""
Pydantic Schemas for API Validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ChaseStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    RECEIVED = "received"
    OVERDUE = "overdue"
    ESCALATED = "escalated"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ChaseType(str, Enum):
    LOA = "loa"
    DOCUMENT = "document"
    FORM = "form"


class ClientBase(BaseModel):
    name: str
    email: str
    phone: str
    risk_profile: Optional[str] = None
    last_review_date: Optional[datetime] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChaseItemBase(BaseModel):
    client_id: int
    type: ChaseType
    category: str
    target: str
    description: str
    priority: Priority = Priority.MEDIUM


class ChaseItemCreate(ChaseItemBase):
    pass


class ChaseItemResponse(ChaseItemBase):
    id: int
    status: ChaseStatus
    sent_date: Optional[datetime] = None
    expected_date: Optional[datetime] = None
    received_date: Optional[datetime] = None
    attempts: int
    last_attempt_date: Optional[datetime] = None
    predicted_delay_days: Optional[int] = None
    agent_actions: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentActivityResponse(BaseModel):
    id: int
    agent_type: str
    action: str
    target: str
    status: str
    details: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class CommunicationBase(BaseModel):
    chase_item_id: int
    channel: str
    direction: str
    recipient: str
    subject: Optional[str] = None
    content: str


class CommunicationResponse(CommunicationBase):
    id: int
    sent_at: datetime
    read: bool
    
    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_chase_items: int
    pending_items: int
    overdue_items: int
    completed_today: int
    avg_completion_days: float
    time_saved_hours: float
    automation_rate: float
    active_agents: int


class AgentStatus(BaseModel):
    agent_type: str
    status: str
    last_action: Optional[str] = None
    last_action_time: Optional[datetime] = None
    items_processed: int


class PredictionResult(BaseModel):
    chase_item_id: int
    predicted_delay_days: int
    confidence: float
    risk_factors: List[str]
    recommendation: str
