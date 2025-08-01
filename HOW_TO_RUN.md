# 🚀 How to Run the Digital Skills Assessment Platform

## Quick Start

### Option 1: One-Command Start (Recommended)
```bash
python run.py
```

This will:
- ✅ Start the backend server on port 8000
- ✅ Start the frontend server on port 8080  
- ✅ Open the app in your browser
- ✅ Run integration tests
- ✅ Handle graceful shutdown with Ctrl+C

### Option 2: Manual Setup

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Start Backend
```bash
# Terminal 1
uvicorn my-rag-bot.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Step 3: Start Frontend
```bash
# Terminal 2
python -m http.server 8080
```

#### Step 4: Open Browser
```
http://localhost:8080/ui/index.html
```

## 📱 Application URLs

- **Main App**: http://localhost:8080/ui/index.html
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Troubleshooting

### If backend fails to start:
1. Check if port 8000 is free: `netstat -an | findstr :8000`
2. Install dependencies: `pip install -r requirements.txt`
3. Check if Ollama is running (optional): `ollama serve`

### If frontend fails to start:
1. Check if port 8080 is free: `netstat -an | findstr :8080`
2. Try a different port: `python -m http.server 8081`

### If you get CORS errors:
- The backend has CORS enabled for all origins
- Make sure both servers are running

## 🎯 Demo Flow

1. **Login**: Enter any email/password
2. **Take Quiz**: Answer 10 digital literacy questions
3. **View Results**: See your score and analysis
4. **Chat with AI**: Ask questions about digital skills
5. **Get Recommendations**: Personalized learning suggestions

## 🏆 Hackathon Features

- ✅ AI-powered RAG bot for intelligent responses
- ✅ Multilingual support (English/Hindi)
- ✅ Skill gap analysis
- ✅ Personalized recommendations
- ✅ Modern, responsive UI
- ✅ Real-time chat interface
- ✅ Comprehensive quiz system

## 📁 File Structure

```
├── run.py                    # Main runner script
├── my-rag-bot/
│   ├── main.py              # FastAPI backend
│   └── rag_bot.py           # RAG bot implementation
├── ui/
│   ├── index.html           # Main quiz interface
│   ├── digital-skills-analyzer.html  # Results & chat
│   ├── script.js            # Frontend logic
│   └── style.css            # Styling
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🛑 Stopping the Application

Press `Ctrl+C` in the terminal where you ran `python run.py`

The application will gracefully shut down both servers. 