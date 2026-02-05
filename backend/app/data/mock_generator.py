"""
Mock Data Generator
Generates realistic client and chase data for demo
"""
from faker import Faker
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

fake = Faker('en_GB')  # UK locale


class MockDataGenerator:
    """Generate realistic mock data for financial advisors"""
    
    def __init__(self):
        self.providers = [
            "Aviva", "Legal & General", "Scottish Widows", 
            "Standard Life", "Prudential", "Aegon",
            "Royal London", "Zurich"
        ]
        
        self.document_types = [
            "Proof of Identity (Passport)",
            "Proof of Address (Utility Bill)",
            "Current Pension Statement",
            "Investment Valuation",
            "P60 Tax Document",
            "Bank Statements (3 months)",
            "Payslips (3 months)",
            "Protection Policy Documents"
        ]
        
        self.loa_types = [
            "Pension Transfer LOA",
            "Investment Account LOA",
            "Protection Policy LOA",
            "ISA Transfer LOA"
        ]
    
    def generate_clients(self, count: int = 20) -> List[Dict[str, Any]]:
        """Generate realistic client data"""
        clients = []
        
        for i in range(count):
            client = {
                "id": i + 1,
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "advisor_id": 1,
                "risk_profile": random.choice(["Conservative", "Moderate", "Balanced", "Growth", "Aggressive"]),
                "last_review_date": fake.date_between(start_date='-2y', end_date='today'),
                "status": "active",
                "created_at": fake.date_between(start_date='-5y', end_date='-1y')
            }
            clients.append(client)
        
        return clients
    
    def generate_chase_items(self, client_ids: List[int], count: int = 50) -> List[Dict[str, Any]]:
        """Generate realistic chase items"""
        chase_items = []
        
        for i in range(count):
            is_loa = random.random() < 0.4  # 40% are LOAs
            
            if is_loa:
                item = self._generate_loa_item(i + 1, client_ids)
            else:
                item = self._generate_document_item(i + 1, client_ids)
            
            chase_items.append(item)
        
        return chase_items
    
    def _generate_loa_item(self, item_id: int, client_ids: List[int]) -> Dict[str, Any]:
        """Generate LOA chase item"""
        provider = random.choice(self.providers)
        sent_date = fake.date_between(start_date='-60d', end_date='-1d')
        
        # Calculate status based on days elapsed
        days_elapsed = (datetime.now().date() - sent_date).days
        expected_days = random.randint(10, 20)
        
        status = self._determine_status(days_elapsed, expected_days)
        attempts = self._determine_attempts(days_elapsed, expected_days)
        
        return {
            "id": item_id,
            "client_id": random.choice(client_ids),
            "type": "loa",
            "category": "provider",
            "target": provider,
            "description": random.choice(self.loa_types),
            "status": status,
            "priority": self._determine_priority(status, days_elapsed),
            "sent_date": sent_date,
            "expected_date": sent_date + timedelta(days=expected_days),
            "received_date": self._determine_received_date(status, sent_date, days_elapsed),
            "attempts": attempts,
            "last_attempt_date": sent_date + timedelta(days=attempts * 7) if attempts > 0 else None,
            "predicted_delay_days": None,
            "agent_actions": [],
            "created_at": sent_date,
            "updated_at": datetime.now()
        }
    
    def _generate_document_item(self, item_id: int, client_ids: List[int]) -> Dict[str, Any]:
        """Generate client document chase item"""
        client_name = fake.name()
        sent_date = fake.date_between(start_date='-45d', end_date='-1d')
        
        days_elapsed = (datetime.now().date() - sent_date).days
        expected_days = random.randint(5, 14)
        
        status = self._determine_status(days_elapsed, expected_days)
        attempts = self._determine_attempts(days_elapsed, expected_days)
        
        return {
            "id": item_id,
            "client_id": random.choice(client_ids),
            "type": "document",
            "category": "client",
            "target": client_name,
            "description": random.choice(self.document_types),
            "status": status,
            "priority": self._determine_priority(status, days_elapsed),
            "sent_date": sent_date,
            "expected_date": sent_date + timedelta(days=expected_days),
            "received_date": self._determine_received_date(status, sent_date, days_elapsed),
            "attempts": attempts,
            "last_attempt_date": sent_date + timedelta(days=attempts * 5) if attempts > 0 else None,
            "predicted_delay_days": None,
            "agent_actions": [],
            "created_at": sent_date,
            "updated_at": datetime.now()
        }
    
    def _determine_status(self, days_elapsed: int, expected_days: int) -> str:
        """Determine item status based on timeline"""
        if random.random() < 0.2:  # 20% received
            return "received"
        elif days_elapsed > expected_days + 7:
            return "overdue"
        elif days_elapsed > expected_days:
            return "sent"
        else:
            return "pending"
    
    def _determine_attempts(self, days_elapsed: int, expected_days: int) -> int:
        """Determine number of chase attempts"""
        if days_elapsed < expected_days:
            return 0
        elif days_elapsed < expected_days + 7:
            return 1
        elif days_elapsed < expected_days + 14:
            return 2
        else:
            return min(3, (days_elapsed - expected_days) // 7)
    
    def _determine_priority(self, status: str, days_elapsed: int) -> str:
        """Determine priority based on status and timeline"""
        if status == "overdue":
            return "urgent" if days_elapsed > 30 else "high"
        elif status == "sent" and days_elapsed > 14:
            return "high"
        elif days_elapsed > 7:
            return "medium"
        else:
            return "low"
    
    def _determine_received_date(self, status: str, sent_date, days_elapsed: int):
        """Determine received date if applicable"""
        if status == "received":
            return sent_date + timedelta(days=random.randint(1, days_elapsed))
        return None
    
    def generate_agent_activities(self, chase_item_ids: List[int], count: int = 100) -> List[Dict[str, Any]]:
        """Generate agent activity logs"""
        activities = []
        
        agent_types = ["document_chaser", "loa_chaser", "predictor", "orchestrator"]
        actions = [
            "Sent reminder email",
            "Placed chase phone call",
            "Generated delay prediction",
            "Escalated to advisor",
            "Updated status",
            "Analyzed response pattern",
            "Sent SMS reminder",
            "Created escalation ticket"
        ]
        
        for i in range(count):
            activity = {
                "id": i + 1,
                "agent_type": random.choice(agent_types),
                "action": random.choice(actions),
                "target": fake.company() if random.random() < 0.4 else fake.name(),
                "status": random.choice(["success"] * 8 + ["failed"] * 2),  # 80% success rate
                "details": fake.sentence(),
                "chase_item_id": random.choice(chase_item_ids) if random.random() < 0.7 else None,
                "timestamp": fake.date_time_between(start_date='-30d', end_date='now')
            }
            activities.append(activity)
        
        return activities
    
    def generate_communications(self, chase_item_ids: List[int], count: int = 150) -> List[Dict[str, Any]]:
        """Generate communication logs"""
        communications = []
        
        for i in range(count):
            channel = random.choice(["email", "sms", "phone"])
            
            comm = {
                "id": i + 1,
                "chase_item_id": random.choice(chase_item_ids),
                "channel": channel,
                "direction": random.choice(["outbound"] * 7 + ["inbound"] * 3),  # 70% outbound
                "recipient": fake.email() if channel == "email" else fake.phone_number(),
                "subject": fake.sentence() if channel == "email" else None,
                "content": fake.paragraph(),
                "sent_at": fake.date_time_between(start_date='-30d', end_date='now'),
                "read": random.choice([True, False])
            }
            communications.append(comm)
        
        return communications


# Convenience function
def generate_full_mock_dataset():
    """Generate complete mock dataset"""
    generator = MockDataGenerator()
    
    clients = generator.generate_clients(20)
    client_ids = [c["id"] for c in clients]
    
    chase_items = generator.generate_chase_items(client_ids, 50)
    chase_item_ids = [item["id"] for item in chase_items]
    
    activities = generator.generate_agent_activities(chase_item_ids, 100)
    communications = generator.generate_communications(chase_item_ids, 150)
    
    return {
        "clients": clients,
        "chase_items": chase_items,
        "activities": activities,
        "communications": communications
    }
