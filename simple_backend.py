#!/usr/bin/env python3
"""
Simple backend server for Digital Skills Assessment
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI(title="Digital Skills Assessment API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class UserProfile(BaseModel):
    name: str
    age: int
    goal: str
    experience: str

class QuizAnswer(BaseModel):
    question_id: int
    selected_answer: int
    time_taken: float = 0.0

class QuizSubmission(BaseModel):
    user_id: str
    answers: List[QuizAnswer]
    total_time: float

class ChatMessage(BaseModel):
    message: str
    user_id: str = "anonymous"

# Quiz questions
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": {
            "en": "What is a URL?",
            "hi": "URL क्या है?"
        },
        "options": {
            "en": ["A software program", "A web address", "A computer virus", "A programming code"],
            "hi": ["एक सॉफ्टवेयर प्रोग्राम", "एक वेब पता", "एक कंप्यूटर वायरस", "एक प्रोग्रामिंग कोड"]
        },
        "correct": 1,
        "skill": "Web Fundamentals",
        "difficulty": "Basic"
    },
    {
        "id": 2,
        "question": {
            "en": "What does HTTPS stand for?",
            "hi": "HTTPS का क्या मतलब है?"
        },
        "options": {
            "en": ["Hyper Text Transfer Protocol Secure", "High Transfer Protocol", "Home Tool Transfer", "HTTP Secure"],
            "hi": ["हाइपर टेक्स्ट ट्रांसफर प्रोटोकॉल सिक्योर", "हाई ट्रांसफर प्रोटोकॉल", "होम टूल ट्रांसफर", "HTTP सिक्योर"]
        },
        "correct": 0,
        "skill": "Cybersecurity",
        "difficulty": "Intermediate"
    },
    {
        "id": 3,
        "question": {
            "en": "What is phishing?",
            "hi": "फिशिंग क्या है?"
        },
        "options": {
            "en": ["A type of fishing game", "A cyber attack using fake emails", "A computer virus", "A software bug"],
            "hi": ["एक प्रकार का मछली पकड़ने का खेल", "फर्जी ईमेल का उपयोग करने वाला साइबर हमला", "एक कंप्यूटर वायरस", "एक सॉफ्टवेयर बग"]
        },
        "correct": 1,
        "skill": "Cybersecurity",
        "difficulty": "Intermediate"
    },
    {
        "id": 4,
        "question": {
            "en": "Which is a strong password?",
            "hi": "कौन सा एक मजबूत पासवर्ड है?"
        },
        "options": {
            "en": ["123456", "password123", "MyP@ssw0rd!", "qwerty"],
            "hi": ["123456", "password123", "MyP@ssw0rd!", "qwerty"]
        },
        "correct": 2,
        "skill": "Cybersecurity",
        "difficulty": "Basic"
    },
    {
        "id": 5,
        "question": {
            "en": "What is two-factor authentication?",
            "hi": "दो-कारक प्रमाणीकरण क्या है?"
        },
        "options": {
            "en": ["Using two passwords", "A second verification step", "Two usernames", "Double login"],
            "hi": ["दो पासवर्ड का उपयोग", "एक दूसरा सत्यापन कदम", "दो यूजरनेम", "डबल लॉगिन"]
        },
        "correct": 1,
        "skill": "Cybersecurity",
        "difficulty": "Intermediate"
    },
    {
        "id": 6,
        "question": {
            "en": "What is a browser?",
            "hi": "ब्राउज़र क्या है?"
        },
        "options": {
            "en": ["A search engine", "A web application", "A computer program", "An internet service"],
            "hi": ["एक सर्च इंजन", "एक वेब एप्लिकेशन", "एक कंप्यूटर प्रोग्राम", "एक इंटरनेट सेवा"]
        },
        "correct": 2,
        "skill": "Web Fundamentals",
        "difficulty": "Basic"
    },
    {
        "id": 7,
        "question": {
            "en": "What is a cookie in web browsing?",
            "hi": "वेब ब्राउज़िंग में कुकी क्या है?"
        },
        "options": {
            "en": ["A type of food", "A small data file", "A virus", "A website"],
            "hi": ["एक प्रकार का भोजन", "एक छोटी डेटा फाइल", "एक वायरस", "एक वेबसाइट"]
        },
        "correct": 1,
        "skill": "Web Fundamentals",
        "difficulty": "Intermediate"
    },
    {
        "id": 8,
        "question": {
            "en": "What is malware?",
            "hi": "मैलवेयर क्या है?"
        },
        "options": {
            "en": ["A type of software", "Malicious software", "A computer game", "A web browser"],
            "hi": ["एक प्रकार का सॉफ्टवेयर", "दुर्भावनापूर्ण सॉफ्टवेयर", "एक कंप्यूटर गेम", "एक वेब ब्राउज़र"]
        },
        "correct": 1,
        "skill": "Cybersecurity",
        "difficulty": "Intermediate"
    },
    {
        "id": 9,
        "question": {
            "en": "What is a VPN?",
            "hi": "VPN क्या है?"
        },
        "options": {
            "en": ["A video game", "Virtual Private Network", "A website", "A computer virus"],
            "hi": ["एक वीडियो गेम", "वर्चुअल प्राइवेट नेटवर्क", "एक वेबसाइट", "एक कंप्यूटर वायरस"]
        },
        "correct": 1,
        "skill": "Cybersecurity",
        "difficulty": "Advanced"
    },
    {
        "id": 10,
        "question": {
            "en": "What is the purpose of a firewall?",
            "hi": "फायरवॉल का उद्देश्य क्या है?"
        },
        "options": {
            "en": ["To block websites", "To protect against unauthorized access", "To speed up internet", "To store files"],
            "hi": ["वेबसाइटों को ब्लॉक करने के लिए", "अनधिकृत पहुंच से बचाने के लिए", "इंटरनेट को तेज करने के लिए", "फाइलें संग्रहीत करने के लिए"]
        },
        "correct": 1,
        "skill": "Cybersecurity",
        "difficulty": "Advanced"
    }
]

# Store user data
user_profiles = {}
quiz_results = {}
chat_history = {}

@app.get("/")
def home():
    return {"message": "Digital Skills Assessment API is running!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "rag_bot": "not_available"}

@app.post("/profile")
def save_profile(profile: UserProfile):
    user_id = f"user_{len(user_profiles) + 1}"
    user_profiles[user_id] = profile.dict()
    
    return {"message": "Profile saved successfully!", "user_id": user_id, "profile": profile.dict()}

@app.get("/quiz/questions")
def get_quiz_questions():
    """Get all quiz questions"""
    return {"questions": QUIZ_QUESTIONS, "total": len(QUIZ_QUESTIONS)}

@app.get("/quiz/questions/{language}")
def get_quiz_questions_by_language(language: str):
    """Get quiz questions in specific language"""
    if language not in ["en", "hi"]:
        raise HTTPException(status_code=400, detail="Language not supported")
    
    questions = []
    for q in QUIZ_QUESTIONS:
        question_data = {
            "id": q["id"],
            "question": q["question"][language],
            "options": q["options"][language],
            "skill": q["skill"],
            "difficulty": q["difficulty"]
        }
        questions.append(question_data)
    
    return {"questions": questions, "total": len(questions)}

@app.post("/quiz/submit")
def submit_quiz(submission: QuizSubmission):
    """Submit quiz answers and get results"""
    if submission.user_id not in user_profiles:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    # Calculate results
    correct_answers = 0
    skill_analysis = {}
    difficulty_analysis = {}
    
    for answer in submission.answers:
        question = next((q for q in QUIZ_QUESTIONS if q["id"] == answer.question_id), None)
        if question:
            is_correct = answer.selected_answer == question["correct"]
            if is_correct:
                correct_answers += 1
            
            # Track skill performance
            skill = question["skill"]
            difficulty = question["difficulty"]
            
            if skill not in skill_analysis:
                skill_analysis[skill] = {"correct": 0, "total": 0}
            if difficulty not in difficulty_analysis:
                difficulty_analysis[difficulty] = {"correct": 0, "total": 0}
            
            skill_analysis[skill]["total"] += 1
            difficulty_analysis[difficulty]["total"] += 1
            
            if is_correct:
                skill_analysis[skill]["correct"] += 1
                difficulty_analysis[difficulty]["correct"] += 1
    
    # Calculate percentages
    for skill in skill_analysis:
        skill_analysis[skill]["percentage"] = round(
            (skill_analysis[skill]["correct"] / skill_analysis[skill]["total"]) * 100
        )
    
    for difficulty in difficulty_analysis:
        difficulty_analysis[difficulty]["percentage"] = round(
            (difficulty_analysis[difficulty]["correct"] / difficulty_analysis[difficulty]["total"]) * 100
        )
    
    total_score = round((correct_answers / len(submission.answers)) * 100)
    
    # Store results
    quiz_results[submission.user_id] = {
        "score": correct_answers,
        "total": len(submission.answers),
        "percentage": total_score,
        "skill_analysis": skill_analysis,
        "difficulty_analysis": difficulty_analysis,
        "time_taken": submission.total_time,
        "answers": [answer.dict() for answer in submission.answers]
    }
    
    return {
        "user_id": submission.user_id,
        "score": correct_answers,
        "total": len(submission.answers),
        "percentage": total_score,
        "skill_analysis": skill_analysis,
        "difficulty_analysis": difficulty_analysis,
        "time_taken": submission.total_time
    }

@app.get("/quiz/results/{user_id}")
def get_quiz_results(user_id: str):
    """Get quiz results for a user"""
    if user_id not in quiz_results:
        raise HTTPException(status_code=404, detail="Quiz results not found")
    
    return quiz_results[user_id]

@app.post("/chat")
async def chat_with_bot(message: ChatMessage):
    """Chat with the bot"""
    try:
        # Simple fallback responses
        fallback_responses = [
            "I'm here to help you with digital skills! What would you like to know?",
            "Welcome to the Digital Skills Assessment Platform! How can I assist you today?",
            "I can help you learn about digital literacy, online safety, and technology skills. What's on your mind?",
            "Feel free to ask me about digital skills, internet safety, or technology topics!",
            "I'm your digital skills assistant. What would you like to learn about today?"
        ]
        import random
        response = random.choice(fallback_responses)
        
        # Store chat history
        if message.user_id not in chat_history:
            chat_history[message.user_id] = []
        
        chat_history[message.user_id].append({
            "user_message": message.message,
            "bot_response": response,
            "timestamp": str(datetime.now())
        })
        
        return {
            "response": response,
            "user_id": message.user_id,
            "timestamp": str(datetime.now())
        }
    except Exception as e:
        return {
            "response": "I'm sorry, I'm having trouble processing your request right now. Please try again later.",
            "error": str(e),
            "user_id": message.user_id
        }

@app.get("/chat/history/{user_id}")
def get_chat_history(user_id: str):
    """Get chat history for a user"""
    if user_id not in chat_history:
        return {"history": []}
    
    return {"history": chat_history[user_id]}

@app.get("/users/{user_id}/profile")
def get_user_profile(user_id: str):
    """Get user profile"""
    if user_id not in user_profiles:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    return {"user_id": user_id, "profile": user_profiles[user_id]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 