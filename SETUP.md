# 🚀 ChaseFlow AI - Setup & Run Guide

## Quick Start (5 Minutes)

Get ChaseFlow AI running in 5 minutes with these simple steps.

---

## Prerequisites

Make sure you have these installed:

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Git** (optional, for cloning)

Check your versions:
```bash
python --version  # Should be 3.11 or higher
node --version    # Should be 18 or higher
npm --version     # Should be 9 or higher
```

---

## Step 1: Navigate to Project

```bash
cd ChaseFlow-AI
```

---

## Step 2: Backend Setup

### 2.1 Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note:** If you encounter issues, try:
```bash
pip install --break-system-packages -r requirements.txt
```

### 2.2 Create Environment File (Optional)

```bash
cp .env.example .env
```

The defaults work fine for development. No changes needed!

### 2.3 Start the Backend

```bash
python -m app.main
```

**OR**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend is running!** 
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

The backend will automatically:
- Create the SQLite database
- Load realistic mock data (20 clients, 50 chase items, 100+ activities)
- Start all autonomous agents

**Keep this terminal open and running.**

---

## Step 3: Frontend Setup

### 3.1 Open a NEW Terminal

Navigate to frontend directory:

```bash
cd ChaseFlow-AI/frontend
```

### 3.2 Install Node Dependencies

```bash
npm install
```

This will install:
- React 18
- Vite (build tool)
- Lucide React (icons)
- Date-fns (date formatting)
- Recharts (optional, for charts)

### 3.3 Start the Frontend

```bash
npm run dev
```

✅ **Frontend is running!**
- Web App: http://localhost:5173

**Keep this terminal open too.**

---

## Step 4: Access ChaseFlow AI

Open your browser and go to:

### 🎉 http://localhost:5173

You should see:
- Beautiful dashboard with stats
- Real-time agent activity
- 50+ chase items being managed
- Live updates every few seconds

---

## 📊 What You'll See

### Dashboard Tab
- **50 Chase Items** across clients and providers
- **4 Active Agents** running autonomously
- **15+ Hours Time Saved** per week
- **80%+ Automation Rate**

### Agent Monitor Tab
- Live agent status (Document Chaser, LOA Chaser, Predictor, Orchestrator)
- Real-time activity stream
- Success/failure tracking
- Full audit trail

### Chase Timeline Tab
- Complete view of all chase items
- Filter by status (Pending, Sent, Overdue, Received)
- Priority badges
- Attempt counts

### Clients Tab
- 20 mock clients
- Risk profiles
- Contact information
- Client status

### Analytics Tab
- Status distribution
- Category breakdown
- Priority analysis
- Activity trends

---

## 🎬 Demo Walkthrough

### 1. **Explore the Dashboard**
   - Check out the 4 stat cards showing key metrics
   - Scroll down to see recent chase items
   - Notice the agent activities being logged

### 2. **Watch the Agents Work**
   - Go to "Agent Monitor" tab
   - See all 4 agents and their statuses
   - Watch the live activity stream
   - Notice how different agents handle different tasks

### 3. **Check the Timeline**
   - Go to "Chase Timeline" tab
   - Filter by "Overdue" to see urgent items
   - Notice provider-specific patterns (Prudential is slower!)
   - See how attempts escalate over time

### 4. **View Analytics**
   - Go to "Analytics" tab
   - See distribution of statuses
   - Notice the balance between client vs provider chases
   - Understand priority distribution

---

## 🔧 Troubleshooting

### Backend won't start?

**Error: "Module not found"**
```bash
pip install -r requirements.txt --break-system-packages
```

**Error: "Port 8000 already in use"**
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9
# Or change the port in backend/app/config.py
```

### Frontend won't start?

**Error: "npm command not found"**
- Install Node.js from nodejs.org

**Error: "Port 5173 already in use"**
```bash
# The frontend will automatically try 5174
# Or kill the process
lsof -ti:5173 | xargs kill -9
```

### Can't connect to backend?

1. Make sure backend is running (check http://localhost:8000/health)
2. Check CORS settings in `backend/app/config.py`
3. Try accessing API docs: http://localhost:8000/docs

### No data showing?

1. Check browser console for errors (F12)
2. Verify API is responding: http://localhost:8000/api/dashboard/stats
3. Restart both backend and frontend

---

## 🎯 Testing Specific Features

### Test the Predictor Agent
```bash
curl http://localhost:8000/api/predictions/1
```

### Manually Process a Chase Item
```bash
curl -X POST http://localhost:8000/api/chase-items/1/process
```

### Check Agent Statuses
```bash
curl http://localhost:8000/api/agents/status
```

### View Analytics
```bash
curl http://localhost:8000/api/analytics/overview
```

---

## 📱 API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser!

---

## 🛠️ Development Tips

### Hot Reload
Both backend and frontend have hot reload enabled:
- **Backend**: Edit Python files → Auto-reloads
- **Frontend**: Edit React files → Instant updates

### Viewing Logs
Backend logs appear in the terminal where you ran `python -m app.main`

### Database Location
- File: `backend/chaseflow.db`
- To reset: Delete the file and restart backend
- To view: Use any SQLite browser

### Mock Data
- Generated automatically on first run
- Located in `backend/app/data/mock_generator.py`
- Customize if needed (20 clients, 50 chase items by default)

---

## 🚀 Production Deployment

For hackathon demo or production:

### Backend (Option 1: Local)
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Backend (Option 2: Docker)
```bash
cd backend
docker build -t chaseflow-backend .
docker run -p 8000:8000 chaseflow-backend
```

### Frontend Build
```bash
cd frontend
npm run build
# Serves from frontend/dist folder
```

Deploy `dist` folder to:
- Vercel
- Netlify  
- AWS S3 + CloudFront
- Any static hosting

---

## 📖 Next Steps

1. **Customize Mock Data**: Edit `backend/app/data/mock_generator.py`
2. **Add Real Integrations**: Connect to Intelliflo, email providers, etc.
3. **Enhance Agents**: Add more sophisticated ML models
4. **Extend UI**: Add more visualizations and controls

---

## 🆘 Still Having Issues?

Common solutions:
1. Restart both terminals (Ctrl+C then start again)
2. Clear browser cache (Ctrl+Shift+R)
3. Check both terminals for error messages
4. Verify Python and Node versions
5. Make sure you're in the correct directories

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can access http://localhost:5173
- [ ] Dashboard shows statistics
- [ ] Agent Monitor shows 4 agents
- [ ] Data is loading (not all zeros)
- [ ] Activity stream is populating

---

## 🎉 You're Ready!

ChaseFlow AI is now running and ready to impress judges with:
- ✅ Autonomous multi-agent system
- ✅ Real-time monitoring
- ✅ Predictive intelligence
- ✅ Beautiful, professional UI
- ✅ Production-ready architecture

**Good luck with your hackathon submission!** 🚀

---

## 📞 Support

Created for AdvisoryAI Hack-to-Hire Challenge
Challenge 03: Agentic Chaser

Built with ❤️ using FastAPI, React, and autonomous agents.
