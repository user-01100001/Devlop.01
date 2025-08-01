
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple quiz questions
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is a URL?",
        "options": ["A software program", "A web address", "A computer virus", "A programming code"],
        "correct": 1,
        "skill": "Web Fundamentals",
        "difficulty": "Basic"
    },
    {
        "id": 2,
        "question": "What does HTTPS stand for?",
        "options": ["Hyper Text Transfer Protocol Secure", "High Transfer Protocol", "Home Tool Transfer", "HTTP Secure"],
        "correct": 0,
        "skill": "Cybersecurity",
        "difficulty": "Intermediate"
    },
    {
        "id": 3,
        "question": "What is phishing?",
        "options": ["A type of fishing game", "A cyber attack using fake emails", "A computer virus", "A software bug"],
        "correct": 1,
        "skill": "Cybersecurity",
        "difficulty": "Intermediate"
    },
    {
        "id": 4,
        "question": "Which is a strong password?",
        "options": ["123456", "password123", "MyP@ssw0rd!", "qwerty"],
        "correct": 2,
        "skill": "Cybersecurity",
        "difficulty": "Basic"
    },
    {
        "id": 5,
        "question": "What is two-factor authentication?",
        "options": ["Using two passwords", "A second verification step", "Two usernames", "Double login"],
        "correct": 1,
        "skill": "Cybersecurity",
        "difficulty": "Intermediate"
    }
]

@app.get("/")
def home():
    return {"message": "Digital Skills Assessment API is running!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "mode": "simple"}

@app.get("/quiz/questions")
def get_quiz_questions():
    return {"questions": QUIZ_QUESTIONS, "total": len(QUIZ_QUESTIONS)}

@app.get("/quiz/questions/en")
def get_quiz_questions_en():
    return {"questions": QUIZ_QUESTIONS, "total": len(QUIZ_QUESTIONS)}

@app.get("/quiz/questions/hi")
def get_quiz_questions_hi():
    return {"questions": QUIZ_QUESTIONS, "total": len(QUIZ_QUESTIONS)}

class UserProfile(BaseModel):
    name: str
    age: int
    goal: str
    experience: str

@app.post("/profile")
def save_profile(profile: UserProfile):
    user_id = f"user_{int(time.time())}"
    return {"message": "Profile saved successfully!", "user_id": user_id, "profile": profile.dict()}

class QuizSubmission(BaseModel):
    user_id: str
    answers: list
    total_time: float

@app.post("/quiz/submit")
def submit_quiz(submission: QuizSubmission):
    return {
        "user_id": submission.user_id,
        "score": 3,
        "total": 5,
        "percentage": 60,
        "skill_analysis": {
            "Web Fundamentals": {"correct": 1, "total": 1, "percentage": 100},
            "Cybersecurity": {"correct": 2, "total": 4, "percentage": 50}
        },
        "difficulty_analysis": {
            "Basic": {"correct": 1, "total": 2, "percentage": 50},
            "Intermediate": {"correct": 2, "total": 3, "percentage": 67}
        },
        "time_taken": submission.total_time
    }

class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"

@app.post("/chat")
async def chat_with_bot(message: ChatMessage):
    responses = {
        "digital literacy": "Digital literacy refers to the ability to find, evaluate, utilize, share, and create content using digital devices and the internet.",
        "password": "A strong password should include uppercase, lowercase, numbers, and special characters. Avoid common passwords like '123456' or 'password'.",
        "https": "HTTPS stands for HyperText Transfer Protocol Secure. It's the secure version of HTTP that encrypts data for security.",
        "cybersecurity": "Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks."
    }
    
    user_msg = message.message.lower()
    for key, response in responses.items():
        if key in user_msg:
            return {"response": response, "user_id": message.user_id}
    
    return {"response": "I can help you with digital literacy, cybersecurity, passwords, and web fundamentals. What would you like to know?", "user_id": message.user_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
