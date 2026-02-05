"""
LOA Chaser Agent
Handles chasing pension providers for LOA responses
"""
from typing import Dict, Any
from datetime import datetime, timedelta
from app.agents.base_agent import BaseAgent
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class LOAChaserAgent(BaseAgent):
    """
    Autonomous agent that chases pension providers for LOA responses
    """
    
    def __init__(self):
        super().__init__(
            agent_id="loa_chaser_001",
            agent_type="loa_chaser"
        )
        self.provider_knowledge = self._load_provider_knowledge()
    
    async def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an LOA chase item
        """
        self.status = "active"
        
        try:
            # Analyze the provider and timeline
            analysis = await self.analyze(item)
            
            # Determine action
            if analysis["is_overdue"]:
                action_result = await self._chase_provider(item, analysis)
            elif analysis["should_escalate"]:
                action_result = await self._escalate_to_manager(item, analysis)
            else:
                action_result = {"action": "monitor", "details": "Within expected timeframe"}
            
            # Log the action
            self.log_action(
                action=action_result["action"],
                details=action_result["details"],
                status="success"
            )
            
            self.status = "idle"
            return action_result
            
        except Exception as e:
            logger.error(f"Error processing LOA chase: {str(e)}")
            self.status = "error"
            return {"action": "error", "details": str(e), "status": "failed"}
    
    async def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze LOA status against provider-specific timelines
        """
        provider = item.get("target", "Unknown")
        days_since_sent = (datetime.utcnow() - item.get("sent_date", datetime.utcnow())).days
        attempts = item.get("attempts", 0)
        
        # Get provider-specific expected response time
        expected_days = self.provider_knowledge.get(
            provider, 
            {"avg_response_days": 15, "reliability": "medium"}
        )["avg_response_days"]
        
        # Add buffer days (20% tolerance)
        buffer_days = int(expected_days * 0.2)
        overdue_threshold = expected_days + buffer_days
        
        is_overdue = days_since_sent >= overdue_threshold
        should_escalate = attempts >= 3 or days_since_sent >= 30
        
        # Calculate urgency score
        urgency_score = min(100, int((days_since_sent / overdue_threshold) * 100))
        
        return {
            "is_overdue": is_overdue,
            "should_escalate": should_escalate,
            "days_since_sent": days_since_sent,
            "expected_days": expected_days,
            "overdue_by": max(0, days_since_sent - overdue_threshold),
            "urgency_score": urgency_score,
            "attempts": attempts,
            "provider": provider,
            "recommended_action": self._recommend_action(days_since_sent, attempts)
        }
    
    async def _chase_provider(self, item: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chase the provider for LOA response
        """
        provider = analysis["provider"]
        chase_method = self._determine_chase_method(analysis)
        
        message = self._compose_provider_message(item, analysis)
        
        return {
            "action": "provider_chased",
            "details": f"Chased {provider} via {chase_method} - {analysis['overdue_by']} days overdue",
            "method": chase_method,
            "message": message,
            "urgency": analysis["urgency_score"],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _escalate_to_manager(self, item: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Escalate to relationship manager or compliance team
        """
        return {
            "action": "escalated_to_manager",
            "details": f"Escalated {analysis['provider']} LOA after {analysis['attempts']} attempts over {analysis['days_since_sent']} days",
            "reason": "Exceeded maximum attempts or 30-day threshold",
            "recommended_action": "Contact provider relationship manager or file formal complaint",
            "compliance_alert": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _determine_chase_method(self, analysis: Dict[str, Any]) -> str:
        """
        Determine best method to chase provider
        """
        attempts = analysis["attempts"]
        urgency = analysis["urgency_score"]
        
        if attempts == 0 and urgency < 50:
            return "email"
        elif attempts == 1 or urgency < 75:
            return "phone_and_email"
        else:
            return "escalated_phone"
    
    def _recommend_action(self, days_since_sent: int, attempts: int) -> str:
        """
        Recommend specific action based on situation
        """
        if days_since_sent < 10:
            return "monitor"
        elif days_since_sent < 20:
            return "send_polite_reminder"
        elif days_since_sent < 30:
            return "phone_chase_urgent"
        else:
            return "escalate_to_manager"
    
    def _compose_provider_message(self, item: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Compose message for provider
        """
        provider = analysis["provider"]
        client = item.get("client_name", "client")
        reference = item.get("reference_number", "N/A")
        
        if analysis["attempts"] == 0:
            return f"Reference: {reference}. Following up on LOA submitted {analysis['days_since_sent']} days ago for {client}. Please confirm receipt and expected processing timeline."
        
        elif analysis["attempts"] == 1:
            return f"Reference: {reference}. Second follow-up on LOA for {client}, submitted {analysis['days_since_sent']} days ago. This is now {analysis['overdue_by']} days beyond your standard processing time. Please provide status update urgently."
        
        else:
            return f"URGENT - Reference: {reference}. Final follow-up on LOA for {client}. Submitted {analysis['days_since_sent']} days ago with no response. Client is waiting for advice. Please escalate to your relationship manager or provide immediate status update."
    
    def _load_provider_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """
        Load provider-specific knowledge and patterns
        """
        # In production, this would be learned from historical data
        providers = {}
        
        for provider, avg_days in settings.PROVIDER_AVERAGE_RESPONSE_DAYS.items():
            providers[provider] = {
                "avg_response_days": avg_days,
                "reliability": "high" if avg_days < 15 else "medium" if avg_days < 20 else "low",
                "best_contact_method": "email" if avg_days < 15 else "phone",
                "peak_delay_months": ["December", "January", "April"]  # Tax year end
            }
        
        return providers
