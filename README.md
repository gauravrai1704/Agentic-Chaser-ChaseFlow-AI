# ChaseFlow AI 

**Agentic Chaser**

## The Problem We Solve

Financial advisors spend 60-70% of their time on administrative tasks instead of giving advice. The biggest time-sink? Chasing documents and LOAs (Letters of Authority).

**The Chase Nightmare:**
- Multiple document requests per client
- 15-20 day wait times from pension providers
- 30-45 minute phone queues
- Manual tracking of hundreds of chase items
- Constant follow-ups and escalations

**ChaseFlow AI eliminates this friction with autonomous, intelligent agents.**

---

## Key Features

### 1. **Multi-Agent Orchestration**
- **Document Chaser Agent**: Autonomously chases clients for missing documents
- **LOA Chaser Agent**: Manages provider LOA requests with provider-specific intelligence
- **Predictor Agent**: ML-powered delay prediction before problems occur
- **Orchestrator Agent**: Master coordinator managing all agent workflows

### 2. **Predictive Intelligence**
- Predicts delays before they happen
- Risk scoring for every chase item
- Provider-specific pattern recognition
- Smart escalation recommendations

### 3. **Autonomous Communication**
- Multi-channel communication (Email, SMS, Phone)
- Tone adaptation based on attempt count
- Politeness-first approach with gentle escalation
- Template-based messaging with personalization

### 4. **Real-Time Monitoring**
- Live agent activity dashboard
- WebSocket-powered real-time updates
- Comprehensive audit trail for FCA compliance
- ROI tracking and time-saved metrics

### 5. **State Management**
- Tracks every chase item across entire lifecycle
- Provider response time intelligence
- Historical pattern learning
- Smart retry logic with exponential backoff

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │  Agent   │  │ Timeline │  │Analytics │   │
│  │          │  │ Monitor  │  │          │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API / WebSocket
┌───────────────────────────┴─────────────────────────────────┐
│                 BACKEND (FastAPI + Python)                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            ORCHESTRATOR AGENT (Master)              │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐   │    │
│  │  │  Document  │  │    LOA     │  │ Predictor  │   │    │
│  │  │   Chaser   │  │   Chaser   │  │   Agent    │   │    │
│  │  └────────────┘  └────────────┘  └────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │          State Manager + Analytics Engine           │    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                    DATABASE (SQLite)                         │
│    Clients | Chase Items | Activities | Communications      │
└─────────────────────────────────────────────────────────────┘
```

---

## Demo Highlights

### Real Impact Metrics (From Mock Data)
- **50+ Chase Items** being managed autonomously
- **100+ Agent Actions** logged with full audit trail
- **15+ Hours Saved** per week per advisor
- **80%+ Automation Rate** for routine chases
- **12 Days Average** completion time (down from 30+)

### Intelligent Features
- **Provider Knowledge**: Learns that Prudential takes 20 days while L&G takes 12
- **Smart Escalation**: Automatically escalates after 3 attempts or overdue threshold
- **Tone Adaptation**: Friendly → Gentle → Urgent messaging progression
- **Channel Selection**: Email → SMS → Phone based on urgency

---

## Technology Stack

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy + SQLite
- Pydantic for data validation
- WebSockets for real-time updates
- Anthropic Claude API (optional, for enhanced AI)

**Frontend:**
- React 18
- Vite (fast build tool)
- Lucide React (icons)
- Native fetch API (no heavy dependencies)

**DevOps:**
- Single-command setup
- Mock data generator included
- Hot reload for development
- Production-ready architecture


## License

MIT License - Built for educational and competition purposes


