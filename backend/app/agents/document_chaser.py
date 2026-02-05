"""
Document Chaser Agent
Handles chasing clients for missing documents
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class DocumentChaserAgent(BaseAgent):
    """
    Autonomous agent that chases clients for missing documents
    """
    
    def __init__(self):
        super().__init__(
            agent_id="doc_chaser_001",
            agent_type="document_chaser"
        )
        self.politeness_level = "high"
        self.reminder_templates = self._load_templates()
    
    async def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a document chase item
        """
        self.status = "active"
        
        try:
            # Analyze the item
            analysis = await self.analyze(item)
            
            # Determine action based on analysis
            if analysis["should_send_reminder"]:
                action_result = await self._send_reminder(item, analysis)
            elif analysis["should_escalate"]:
                action_result = await self._escalate_to_advisor(item, analysis)
            else:
                action_result = {"action": "monitor", "details": "Item within acceptable timeframe"}
            
            # Log the action
            self.log_action(
                action=action_result["action"],
                details=action_result["details"],
                status="success"
            )
            
            self.status = "idle"
            return action_result
            
        except Exception as e:
            logger.error(f"Error processing document chase: {str(e)}")
            self.status = "error"
            return {"action": "error", "details": str(e), "status": "failed"}
    
    async def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze whether to send a reminder or escalate
        """
        attempts = item.get("attempts", 0)
        days_since_sent = (datetime.utcnow() - item.get("sent_date", datetime.utcnow())).days
        priority = item.get("priority", "medium")
        
        # Determine thresholds based on priority
        thresholds = {
            "urgent": {"reminder_days": 2, "escalation_days": 5},
            "high": {"reminder_days": 4, "escalation_days": 7},
            "medium": {"reminder_days": 7, "escalation_days": 14},
            "low": {"reminder_days": 10, "escalation_days": 21}
        }
        
        threshold = thresholds.get(priority, thresholds["medium"])
        
        should_send_reminder = (
            days_since_sent >= threshold["reminder_days"] and
            attempts < 3 and
            item.get("status") != "received"
        )
        
        should_escalate = (
            days_since_sent >= threshold["escalation_days"] or
            attempts >= 3
        )
        
        return {
            "should_send_reminder": should_send_reminder,
            "should_escalate": should_escalate,
            "days_since_sent": days_since_sent,
            "attempts": attempts,
            "priority": priority,
            "recommended_channel": self._recommend_channel(attempts),
            "tone": self._determine_tone(attempts)
        }
    
    async def _send_reminder(self, item: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a reminder to the client
        """
        channel = analysis["recommended_channel"]
        tone = analysis["tone"]
        
        message = self._compose_message(item, tone, analysis["attempts"])
        
        # In production, this would actually send via email/SMS
        # For now, we log and record the action
        
        return {
            "action": "reminder_sent",
            "details": f"Sent {tone} reminder via {channel} to {item['target']}",
            "channel": channel,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _escalate_to_advisor(self, item: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Escalate to human advisor
        """
        return {
            "action": "escalated",
            "details": f"Escalated to advisor after {analysis['attempts']} attempts over {analysis['days_since_sent']} days",
            "reason": "Multiple attempts without response",
            "recommended_action": "Personal phone call or meeting request",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _recommend_channel(self, attempts: int) -> str:
        """
        Recommend communication channel based on attempt count
        """
        if attempts == 0:
            return "email"
        elif attempts == 1:
            return "sms"
        else:
            return "phone"
    
    def _determine_tone(self, attempts: int) -> str:
        """
        Determine message tone based on attempts
        """
        if attempts == 0:
            return "friendly"
        elif attempts == 1:
            return "gentle_reminder"
        else:
            return "urgent_but_polite"
    
    def _compose_message(self, item: Dict[str, Any], tone: str, attempts: int) -> str:
        """
        Compose message based on tone
        """
        client_name = item.get("target", "").split()[0]  # First name
        document_type = item.get("description", "documents")
        
        templates = {
            "friendly": f"Hi {client_name}, I hope you're doing well! Just a friendly reminder that we're still waiting for your {document_type}. No rush, but whenever you get a chance, it would help us move forward with your advice. Let me know if you need any help!",
            
            "gentle_reminder": f"Hi {client_name}, just following up on our request for {document_type}. I know these things can slip through the cracks! If there's anything unclear or if you're having trouble finding what we need, I'm here to help.",
            
            "urgent_but_polite": f"Hi {client_name}, I wanted to reach out one more time about {document_type}. We really need these to finalize your advice and I don't want any delays on your end. Could you let me know if there's anything blocking you from sending these over? Happy to help in any way!"
        }
        
        return templates.get(tone, templates["friendly"])
    
    def _load_templates(self) -> Dict[str, str]:
        """
        Load message templates
        """
        return {
            "initial": "Initial document request template",
            "reminder_1": "First reminder template",
            "reminder_2": "Second reminder template",
            "final": "Final reminder before escalation"
        }
