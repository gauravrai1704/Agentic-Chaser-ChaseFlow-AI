"""
Database Models for ChaseFlow AI
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    phone = Column(String)
    advisor_id = Column(Integer, default=1)
    risk_profile = Column(String)
    last_review_date = Column(DateTime)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class ChaseItem(Base):
    __tablename__ = "chase_items"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True)
    type = Column(String)  # "loa", "document", "form"
    category = Column(String)  # "client", "provider"
    target = Column(String)  # client name or provider name
    description = Column(String)
    status = Column(String, default="pending")  # pending, sent, received, overdue, escalated
    priority = Column(String, default="medium")  # low, medium, high, urgent
    sent_date = Column(DateTime)
    expected_date = Column(DateTime)
    received_date = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)
    last_attempt_date = Column(DateTime, nullable=True)
    predicted_delay_days = Column(Integer, nullable=True)
    agent_actions = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AgentActivity(Base):
    __tablename__ = "agent_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String)  # document_chaser, loa_chaser, orchestrator, predictor
    action = Column(String)
    target = Column(String)
    status = Column(String)  # success, failed, pending
    details = Column(Text)
    chase_item_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Communication(Base):
    __tablename__ = "communications"
    
    id = Column(Integer, primary_key=True, index=True)
    chase_item_id = Column(Integer)
    channel = Column(String)  # email, sms, phone
    direction = Column(String)  # outbound, inbound
    recipient = Column(String)
    subject = Column(String, nullable=True)
    content = Column(Text)
    sent_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)


class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String)
    metric_value = Column(Float)
    period = Column(String)  # daily, weekly, monthly
    calculated_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize the database"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
