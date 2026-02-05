"""
Multi-Agent Orchestrator
Coordinates all agents and manages workflow
"""
from typing import Dict, Any, List
from datetime import datetime
from app.agents.base_agent import BaseAgent
from app.agents.document_chaser import DocumentChaserAgent
from app.agents.loa_chaser import LOAChaserAgent
from app.agents.predictor import PredictorAgent
import asyncio
import logging

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    """
    Master orchestrator that coordinates all specialized agents
    """
    
    def __init__(self):
        super().__init__(
            agent_id="orchestrator_001",
            agent_type="orchestrator"
        )
        
        # Initialize specialized agents
        self.document_chaser = DocumentChaserAgent()
        self.loa_chaser = LOAChaserAgent()
        self.predictor = PredictorAgent()
        
        self.agents = {
            "document_chaser": self.document_chaser,
            "loa_chaser": self.loa_chaser,
            "predictor": self.predictor
        }
        
    async def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an item by routing to appropriate agent
        """
        self.status = "active"
        
        try:
            # Determine which agent should handle this
            agent = self._route_to_agent(item)
            
            # Get prediction first
            prediction = await self.predictor.analyze(item)
            
            # Process with appropriate agent
            result = await agent.process(item)
            
            # Combine results
            combined_result = {
                "agent_type": agent.agent_type,
                "action": result,
                "prediction": prediction,
                "orchestrator_timestamp": datetime.utcnow().isoformat()
            }
            
            self.log_action(
                action="orchestrated_task",
                details=f"Routed to {agent.agent_type}, action: {result.get('action')}",
                status="success"
            )
            
            self.status = "idle"
            return combined_result
            
        except Exception as e:
            logger.error(f"Orchestration error: {str(e)}")
            self.status = "error"
            return {"error": str(e)}
    
    async def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an item across all agents for comprehensive insights
        """
        # Get analysis from all relevant agents
        analyses = {}
        
        agent = self._route_to_agent(item)
        analyses["primary_agent"] = await agent.analyze(item)
        analyses["prediction"] = await self.predictor.analyze(item)
        
        return analyses
    
    async def process_batch(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple items efficiently
        """
        self.status = "batch_processing"
        
        # Group items by agent type for efficient processing
        grouped = self._group_items_by_agent(items)
        
        results = []
        
        for agent_type, agent_items in grouped.items():
            agent = self.agents[agent_type]
            
            # Process items with this agent
            for item in agent_items:
                result = await self.process(item)
                results.append(result)
        
        self.status = "idle"
        return results
    
    async def get_all_agent_statuses(self) -> List[Dict[str, Any]]:
        """
        Get status of all agents
        """
        statuses = []
        
        for agent_type, agent in self.agents.items():
            statuses.append(agent.get_status())
        
        # Add orchestrator status
        statuses.append(self.get_status())
        
        return statuses
    
    async def run_continuous(self, db_session, interval: int = 30):
        """
        Run continuous monitoring and processing
        This would be called by a background task
        """
        while True:
            try:
                # Get pending items from database
                pending_items = self._get_pending_items(db_session)
                
                if pending_items:
                    logger.info(f"Processing {len(pending_items)} pending items")
                    await self.process_batch(pending_items)
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in continuous run: {str(e)}")
                await asyncio.sleep(interval)
    
    def _route_to_agent(self, item: Dict[str, Any]) -> BaseAgent:
        """
        Determine which agent should handle this item
        """
        item_type = item.get("type")
        category = item.get("category")
        
        if item_type == "loa" or category == "provider":
            return self.loa_chaser
        else:
            return self.document_chaser
    
    def _group_items_by_agent(self, items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group items by which agent should handle them
        """
        grouped = {
            "document_chaser": [],
            "loa_chaser": []
        }
        
        for item in items:
            agent = self._route_to_agent(item)
            agent_type = agent.agent_type
            
            if agent_type in grouped:
                grouped[agent_type].append(item)
        
        return grouped
    
    def _get_pending_items(self, db_session) -> List[Dict[str, Any]]:
        """
        Get items that need processing from database
        This is a placeholder - actual implementation would query the database
        """
        # In production, this would query the database for pending items
        return []
    
    async def simulate_activity(self) -> Dict[str, Any]:
        """
        Simulate agent activity for demo purposes
        """
        import random
        
        agent_types = ["document_chaser", "loa_chaser", "predictor"]
        actions = [
            "Sent reminder email to client",
            "Chased provider via phone",
            "Generated delay prediction",
            "Escalated to advisor",
            "Updated client status",
            "Analyzed response pattern"
        ]
        
        return {
            "agent_type": random.choice(agent_types),
            "action": random.choice(actions),
            "status": "success",
            "timestamp": datetime.utcnow().isoformat()
        }
