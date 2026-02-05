"""
Base Agent Class
All specialized agents inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all autonomous agents in ChaseFlow AI
    """
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = "idle"
        self.last_action = None
        self.last_action_time = None
        self.items_processed = 0
        
    @abstractmethod
    async def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a chase item
        Must be implemented by child classes
        """
        pass
    
    @abstractmethod
    async def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a chase item and return insights
        Must be implemented by child classes
        """
        pass
    
    def log_action(self, action: str, details: str, status: str = "success"):
        """Log an agent action"""
        self.last_action = action
        self.last_action_time = datetime.utcnow()
        self.items_processed += 1
        
        logger.info(f"[{self.agent_type}] {action} - {status}: {details}")
        
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "action": action,
            "details": details,
            "status": status,
            "timestamp": self.last_action_time.isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "last_action": self.last_action,
            "last_action_time": self.last_action_time.isoformat() if self.last_action_time else None,
            "items_processed": self.items_processed
        }
    
    def _should_escalate(self, item: Dict[str, Any]) -> bool:
        """
        Determine if an item should be escalated to human
        """
        # Escalate if overdue by more than threshold
        if item.get("attempts", 0) >= 3:
            return True
        
        # Escalate if high priority and delayed
        if item.get("priority") == "urgent" and item.get("status") == "overdue":
            return True
        
        return False
    
    def _generate_reasoning(self, action: str, context: Dict[str, Any]) -> str:
        """
        Generate Chain-of-Thought reasoning for compliance audit
        """
        reasoning = f"Action: {action}\n"
        reasoning += f"Context: {context}\n"
        reasoning += f"Decision: Based on {len(context)} factors, determined best course of action\n"
        return reasoning
