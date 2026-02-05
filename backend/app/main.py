"""
ChaseFlow AI - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.models.database import init_db, get_db, Base, engine
from app.api.routes import router as api_router
from app.api.websocket import router as ws_router
from app.data.mock_generator import generate_full_mock_dataset
from app.models import database as db_models

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    # Startup
    logger.info("Starting ChaseFlow AI...")
    init_db()
    
    # Load mock data if database is empty
    db = next(get_db())
    if db.query(db_models.Client).count() == 0:
        logger.info("Loading mock data...")
        load_mock_data(db)
    
    yield
    
    # Shutdown
    logger.info("Shutting down ChaseFlow AI...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Autonomous Agent System for Financial Advisor Chase Management",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(ws_router, prefix="/ws")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "message": "Welcome to ChaseFlow AI - Autonomous Agent System for Financial Advisors"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": db_models.datetime.utcnow().isoformat()
    }


def load_mock_data(db: Session):
    """Load mock data into database"""
    try:
        mock_data = generate_full_mock_dataset()
        
        # Load clients
        for client_data in mock_data["clients"]:
            client = db_models.Client(**client_data)
            db.add(client)
        
        # Load chase items
        for item_data in mock_data["chase_items"]:
            chase_item = db_models.ChaseItem(**item_data)
            db.add(chase_item)
        
        # Load activities
        for activity_data in mock_data["activities"]:
            activity = db_models.AgentActivity(**activity_data)
            db.add(activity)
        
        # Load communications
        for comm_data in mock_data["communications"]:
            comm = db_models.Communication(**comm_data)
            db.add(comm)
        
        db.commit()
        logger.info("Mock data loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading mock data: {str(e)}")
        db.rollback()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
