"""
Predictive Delay Engine
Uses ML to predict delays before they happen
"""
from typing import Dict, Any, List
from datetime import datetime
from app.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class PredictorAgent(BaseAgent):
    """
    ML-powered agent that predicts delays and recommends proactive actions
    """
    
    def __init__(self):
        super().__init__(
            agent_id="predictor_001",
            agent_type="predictor"
        )
        self.model_version = "v1.0"
        self.confidence_threshold = 0.7
    
    async def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate predictions for a chase item
        """
        self.status = "active"
        
        try:
            prediction = await self.analyze(item)
            
            # Log the prediction
            self.log_action(
                action="prediction_generated",
                details=f"Predicted {prediction['predicted_delay_days']} day delay with {prediction['confidence']:.0%} confidence",
                status="success"
            )
            
            self.status = "idle"
            return prediction
            
        except Exception as e:
            logger.error(f"Error generating prediction: {str(e)}")
            self.status = "error"
            return {"error": str(e)}
    
    async def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze item and predict potential delays
        """
        # Extract features for prediction
        features = self._extract_features(item)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(features)
        
        # Predict delay
        predicted_delay = self._predict_delay(features, risk_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(features, risk_score, predicted_delay)
        
        return {
            "chase_item_id": item.get("id"),
            "predicted_delay_days": predicted_delay,
            "confidence": risk_score / 100,  # Convert to 0-1 scale
            "risk_factors": self._identify_risk_factors(features),
            "recommendation": recommendations,
            "model_version": self.model_version,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _extract_features(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract features for ML prediction
        """
        return {
            "type": item.get("type"),
            "category": item.get("category"),
            "priority": item.get("priority"),
            "target": item.get("target"),
            "days_since_sent": (datetime.utcnow() - item.get("sent_date", datetime.utcnow())).days,
            "attempts": item.get("attempts", 0),
            "current_month": datetime.utcnow().month,
            "day_of_week": datetime.utcnow().weekday(),
            "is_peak_season": datetime.utcnow().month in [12, 1, 3, 4],  # Tax year transitions
        }
    
    def _calculate_risk_score(self, features: Dict[str, Any]) -> int:
        """
        Calculate risk score (0-100) based on features
        Simple rule-based scoring for demo
        In production, this would be a trained ML model
        """
        score = 0
        
        # Provider/client responsiveness
        if features["category"] == "provider":
            score += 40  # Providers generally slower
        else:
            score += 20
        
        # Time-based factors
        if features["days_since_sent"] > 14:
            score += 20
        elif features["days_since_sent"] > 7:
            score += 10
        
        # Attempt history
        score += features["attempts"] * 10
        
        # Priority
        priority_scores = {"urgent": 15, "high": 10, "medium": 5, "low": 0}
        score += priority_scores.get(features["priority"], 5)
        
        # Seasonal factors
        if features["is_peak_season"]:
            score += 15
        
        # Weekend submission (less likely to be processed quickly)
        if features["day_of_week"] >= 5:
            score += 5
        
        return min(100, score)
    
    def _predict_delay(self, features: Dict[str, Any], risk_score: int) -> int:
        """
        Predict number of days delay
        """
        base_delay = 0
        
        if features["category"] == "provider":
            base_delay = 15  # Average provider response
        else:
            base_delay = 7   # Average client response
        
        # Adjust based on risk score
        delay_multiplier = risk_score / 50  # 0-2x multiplier
        
        predicted = int(base_delay * delay_multiplier)
        
        # Add attempt penalty
        predicted += features["attempts"] * 3
        
        return predicted
    
    def _identify_risk_factors(self, features: Dict[str, Any]) -> List[str]:
        """
        Identify specific risk factors
        """
        factors = []
        
        if features["days_since_sent"] > 14:
            factors.append("Already delayed beyond typical timeline")
        
        if features["attempts"] >= 2:
            factors.append("Multiple chase attempts with no response")
        
        if features["is_peak_season"]:
            factors.append("Peak season - providers experiencing high volume")
        
        if features["category"] == "provider" and features["attempts"] == 0:
            factors.append("Provider LOAs typically take 15-20 days")
        
        if features["day_of_week"] >= 5:
            factors.append("Submitted on weekend - processing may be delayed")
        
        if features["priority"] == "urgent" and features["days_since_sent"] > 3:
            factors.append("Urgent item not responded to quickly")
        
        return factors if factors else ["Low risk - tracking normally"]
    
    def _generate_recommendations(self, features: Dict[str, Any], risk_score: int, predicted_delay: int) -> str:
        """
        Generate actionable recommendations
        """
        if risk_score >= 80:
            return "HIGH RISK: Immediate escalation recommended. Consider direct phone contact with relationship manager."
        
        elif risk_score >= 60:
            return "MODERATE RISK: Proactive chase recommended. Follow up via phone if no response within 48 hours."
        
        elif risk_score >= 40:
            return "LOW-MODERATE RISK: Send friendly reminder. Monitor for response within 5 business days."
        
        else:
            return "LOW RISK: Continue monitoring. Item within expected timeline. No immediate action required."
    
    async def batch_predict(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate predictions for multiple items
        """
        predictions = []
        
        for item in items:
            prediction = await self.analyze(item)
            predictions.append(prediction)
        
        return predictions
