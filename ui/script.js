const loginForm = document.getElementById("login-form");
const loginSection = document.getElementById("login-section");
const quizSection = document.getElementById("quiz-section");
const resultSection = document.getElementById("result-section");
const analysisSection = document.getElementById("analysis-section");
const tracker = document.getElementById("tracker");
const questionBox = document.getElementById("question-box");
const nextBtn = document.getElementById("next-btn");
const analyzeBtn = document.getElementById("analyze-btn");
const retakeBtn = document.getElementById("retake-btn");
const backToLoginBtn = document.getElementById("back-to-login");

// API Configuration
const API_BASE_URL = 'http://localhost:8000';
let currentUserId = null;
let questions = [];
let currentQ = 0;
let score = 7;
let userAnswers = [];
let skillPerformance = {};
let currentLanguage = 'en';
let quizStartTime = null;

// Make questions globally accessible for language switching
window.currentQuestions = questions;
window.currentQuestionIndex = currentQ;

// API Functions
async function fetchQuestions(language = 'en') {
    try {
        const response = await fetch(`${API_BASE_URL}/quiz/questions/${language}`);
        const data = await response.json();
        questions = data.questions;
        window.currentQuestions = questions;
        return questions;
    } catch (error) {
        console.error('Error fetching questions:', error);
        return [];
    }
}

async function submitProfile(profileData) {
    try {
        const response = await fetch(`${API_BASE_URL}/profile`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(profileData)
        });
        const data = await response.json();
        currentUserId = data.user_id;
        localStorage.setItem('currentUserId', currentUserId);
        return data;
    } catch (error) {
        console.error('Error submitting profile:', error);
        throw error;
    }
}

async function submitQuizResults() {
    try {
        const submission = {
            user_id: currentUserId,
            answers: userAnswers.map(answer => ({
                question_id: answer.questionIndex + 1,
                selected_answer: answer.selectedAnswer,
                time_taken: answer.timeTaken || 0
            })),
            total_time: Date.now() - quizStartTime
        };

        const response = await fetch(`${API_BASE_URL}/quiz/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(submission)
        });
        
        const data = await response.json();
        localStorage.setItem('quizResults', JSON.stringify(data));
        return data;
    } catch (error) {
        console.error('Error submitting quiz results:', error);
        throw error;
    }
}

async function chatWithBot(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                user_id: currentUserId || 'anonymous'
            })
        });
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error chatting with bot:', error);
        return "I'm sorry, I'm having trouble connecting to the server right now.";
    }
}

// Event Listeners
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    try {
        // Create user profile
        const profileData = {
            name: email.split('@')[0], // Use email prefix as name
            age: 25, // Default age
            goal: "Improve digital skills",
            experience: "Beginner"
        };
        
        await submitProfile(profileData);
        
        // Load questions
        await fetchQuestions(currentLanguage);
        
        // Start quiz
        loginSection.style.display = "none";
        quizSection.style.display = "block";
        quizStartTime = Date.now();
        loadQuestion();
    } catch (error) {
        alert("Error starting quiz. Please try again.");
        console.error('Login error:', error);
    }
});

nextBtn.addEventListener("click", async () => {
    const selected = document.querySelector('input[name="option"]:checked');
    if (selected) {
        const selectedIndex = parseInt(selected.value);
        const questionStartTime = Date.now() - quizStartTime;
        
        userAnswers.push({
            questionIndex: currentQ,
            selectedAnswer: selectedIndex,
            isCorrect: selectedIndex === questions[currentQ].correct,
            skill: questions[currentQ].skill,
            difficulty: questions[currentQ].difficulty,
            timeTaken: questionStartTime
        });
        
        if (selectedIndex === questions[currentQ].correct) score++;
        
        currentQ++;
        window.currentQuestionIndex = currentQ;
        
        if (currentQ < questions.length) {
            loadQuestion();
        } else {
            // Submit results to backend
            try {
                const results = await submitQuizResults();
                localStorage.setItem('quizResults', JSON.stringify(results));
                window.location.href = 'digital-skills-analyzer.html';
            } catch (error) {
                alert("Error submitting results. Please try again.");
                console.error('Submission error:', error);
            }
        }
    } else {
        const currentLang = localStorage.getItem('selectedLanguage') || 'en';
        const alertMessage = currentLang === 'hi' ? "कृपया जारी रखने से पहले एक उत्तर चुनें।" : "Please select an answer before continuing.";
        alert(alertMessage);
    }
});

analyzeBtn.addEventListener("click", () => {
    resultSection.style.display = "none";
    analysisSection.style.display = "block";
    performSkillGapAnalysis();
});

retakeBtn.addEventListener("click", () => {
    resetQuiz();
    analysisSection.style.display = "none";
    quizSection.style.display = "block";
    loadQuestion();
});

backToLoginBtn.addEventListener("click", () => {
    resetQuiz();
    analysisSection.style.display = "none";
    loginSection.style.display = "block";
});

function loadQuestion() {
    if (questions.length === 0) {
        console.error('No questions loaded');
        return;
    }
    
    const currentLang = localStorage.getItem('selectedLanguage') || 'en';
    const q = questions[currentQ];
    tracker.textContent = `${currentQ + 1}`;
    tracker.style.background = `conic-gradient(red ${(currentQ + 1) / questions.length * 100}%, #333 ${(currentQ + 1) / questions.length * 100}%)`;
    
    displayQuestion(q, currentLang);
}

function displayQuestion(question, lang = 'en') {
    const questionText = question.question;
    const options = question.options;
    
    questionBox.innerHTML = `
        <p>${currentQ + 1}. ${questionText}</p>
        ${options.map((opt, index) => `<label><input type="radio" name="option" value="${index}"> ${opt}</label>`).join('')}
    `;
}

// Global function for language switching (called from HTML)
window.updateQuizLanguage = async function(lang) {
    currentLanguage = lang;
    if (questions.length === 0) {
        await fetchQuestions(lang);
    }
    if (window.currentQuestions && window.currentQuestionIndex !== undefined) {
        const currentQuestion = window.currentQuestions[window.currentQuestionIndex];
        if (currentQuestion) {
            displayQuestion(currentQuestion, lang);
        }
    }
};

function displayResults() {
    const currentLang = localStorage.getItem('selectedLanguage') || 'en';
    const percentage = Math.round((score / questions.length) * 100);
    
    const resultText = currentLang === 'hi' 
        ? `✅ आपने ${questions.length} में से ${score} अंक प्राप्त किए`
        : `✅ You scored ${score} out of ${questions.length}`;
    
    document.getElementById("result-text").textContent = resultText;
    
    const scoreDisplay = document.getElementById("score-display");
    scoreDisplay.innerHTML = `
        <div class="score-percentage">${percentage}%</div>
        <div class="score-bar">
            <div class="score-fill" style="width: ${percentage}%"></div>
        </div>
        <div class="score-level">
            ${getScoreLevel(percentage, currentLang)}
        </div>
    `;
}

function getScoreLevel(percentage, lang = 'en') {
    if (lang === 'hi') {
        if (percentage >= 90) return "🎯 विशेषज्ञ स्तर";
        if (percentage >= 70) return "🚀 उन्नत स्तर";
        if (percentage >= 50) return "📚 मध्यम स्तर";
        if (percentage >= 30) return "🔰 शुरुआती स्तर";
        return "🌱 नौसिखिया स्तर";
    } else {
        if (percentage >= 90) return "🎯 Expert Level";
        if (percentage >= 70) return "🚀 Advanced Level";
        if (percentage >= 50) return "📚 Intermediate Level";
        if (percentage >= 30) return "🔰 Beginner Level";
        return "🌱 Novice Level";
    }
}

function performSkillGapAnalysis() {
    // Analyze performance by skill category
    const skillAnalysis = {};
    const difficultyAnalysis = {};
    
    userAnswers.forEach(answer => {
        const skill = answer.skill;
        const difficulty = answer.difficulty;
        
        if (!skillAnalysis[skill]) {
            skillAnalysis[skill] = { correct: 0, total: 0 };
        }
        if (!difficultyAnalysis[difficulty]) {
            difficultyAnalysis[difficulty] = { correct: 0, total: 0 };
        }
        
        skillAnalysis[skill].total++;
        difficultyAnalysis[difficulty].total++;
        
        if (answer.isCorrect) {
            skillAnalysis[skill].correct++;
            difficultyAnalysis[difficulty].correct++;
        }
    });
    
    // Calculate percentages
    Object.keys(skillAnalysis).forEach(skill => {
        skillAnalysis[skill].percentage = Math.round((skillAnalysis[skill].correct / skillAnalysis[skill].total) * 100);
    });
    
    Object.keys(difficultyAnalysis).forEach(difficulty => {
        difficultyAnalysis[difficulty].percentage = Math.round((difficultyAnalysis[difficulty].correct / difficultyAnalysis[difficulty].total) * 100);
    });
    
    displayAnalysis(skillAnalysis, difficultyAnalysis);
    generateRecommendations(skillAnalysis, difficultyAnalysis);
}

function displayAnalysis(skillAnalysis, difficultyAnalysis) {
    const currentLang = localStorage.getItem('selectedLanguage') || 'en';
    const analysisContent = document.getElementById("analysis-content");
    
    let analysisHTML = '<div class="analysis-grid">';
    
    // Skill-based analysis
    const skillTitle = currentLang === 'hi' ? '📊 कौशल प्रदर्शन' : '📊 Skill Performance';
    analysisHTML += '<div class="analysis-section">';
    analysisHTML += `<h3>${skillTitle}</h3>`;
    
    Object.keys(skillAnalysis).forEach(skill => {
        const data = skillAnalysis[skill];
        const strength = data.percentage >= 70 ? 'strong' : data.percentage >= 50 ? 'moderate' : 'weak';
        const emoji = data.percentage >= 70 ? '✅' : data.percentage >= 50 ? '⚠️' : '❌';
        
        analysisHTML += `
            <div class="skill-item ${strength}">
                <div class="skill-header">
                    <span>${emoji} ${skill}</span>
                    <span class="skill-score">${data.percentage}%</span>
                </div>
                <div class="skill-bar">
                    <div class="skill-fill ${strength}" style="width: ${data.percentage}%"></div>
                </div>
                <div class="skill-details">${data.correct}/${data.total} correct</div>
            </div>
        `;
    });
    
    analysisHTML += '</div>';
    
    // Difficulty-based analysis
    const difficultyTitle = currentLang === 'hi' ? '🎯 कठिनाई स्तर प्रदर्शन' : '🎯 Difficulty Level Performance';
    analysisHTML += '<div class="analysis-section">';
    analysisHTML += `<h3>${difficultyTitle}</h3>`;
    
    Object.keys(difficultyAnalysis).forEach(difficulty => {
        const data = difficultyAnalysis[difficulty];
        const strength = data.percentage >= 70 ? 'strong' : data.percentage >= 50 ? 'moderate' : 'weak';
        const emoji = data.percentage >= 70 ? '✅' : data.percentage >= 50 ? '⚠️' : '❌';
        
        analysisHTML += `
            <div class="difficulty-item ${strength}">
                <div class="difficulty-header">
                    <span>${emoji} ${difficulty}</span>
                    <span class="difficulty-score">${data.percentage}%</span>
                </div>
                <div class="difficulty-bar">
                    <div class="difficulty-fill ${strength}" style="width: ${data.percentage}%"></div>
                </div>
                <div class="difficulty-details">${data.correct}/${data.total} correct</div>
            </div>
        `;
    });
    
    analysisHTML += '</div></div>';
    
    analysisContent.innerHTML = analysisHTML;
}

function generateRecommendations(skillAnalysis, difficultyAnalysis) {
    const currentLang = localStorage.getItem('selectedLanguage') || 'en';
    const recommendationsDiv = document.getElementById("recommendations");
    const recommendationsTitle = currentLang === 'hi' ? '💡 व्यक्तिगत सिफारिशें' : '💡 Personalized Recommendations';
    let recommendationsHTML = `<h3>${recommendationsTitle}</h3>`;
    
    // Identify weak areas
    const weakSkills = Object.keys(skillAnalysis).filter(skill => skillAnalysis[skill].percentage < 50);
    const weakDifficulties = Object.keys(difficultyAnalysis).filter(difficulty => difficultyAnalysis[difficulty].percentage < 50);
    
    recommendationsHTML += '<div class="recommendations-list">';
    
    if (weakSkills.length > 0) {
        const skillsTitle = currentLang === 'hi' ? '🔧 सुधार के लिए कौशल' : '🔧 Skills to Improve';
        recommendationsHTML += '<div class="recommendation-category">';
        recommendationsHTML += `<h4>${skillsTitle}</h4>`;
        weakSkills.forEach(skill => {
            recommendationsHTML += `<div class="recommendation-item">
                <strong>${skill}:</strong> ${getSkillRecommendations(skill, currentLang)}
            </div>`;
        });
        recommendationsHTML += '</div>';
    }
    
    if (weakDifficulties.length > 0) {
        const difficultyTitle = currentLang === 'hi' ? '📈 कठिनाई स्तर फोकस' : '📈 Difficulty Level Focus';
        recommendationsHTML += '<div class="recommendation-category">';
        recommendationsHTML += `<h4>${difficultyTitle}</h4>`;
        weakDifficulties.forEach(difficulty => {
            recommendationsHTML += `<div class="recommendation-item">
                <strong>${difficulty} Level:</strong> ${getDifficultyRecommendations(difficulty, currentLang)}
            </div>`;
        });
        recommendationsHTML += '</div>';
    }
    
    // Overall recommendations
    const overallScore = Math.round((score / questions.length) * 100);
    const nextStepsTitle = currentLang === 'hi' ? '🎯 अगले कदम' : '🎯 Next Steps';
    recommendationsHTML += '<div class="recommendation-category">';
    recommendationsHTML += `<h4>${nextStepsTitle}</h4>`;
    recommendationsHTML += `<div class="recommendation-item">${getOverallRecommendations(overallScore, currentLang)}</div>`;
    recommendationsHTML += '</div>';
    
    recommendationsHTML += '</div>';
    recommendationsDiv.innerHTML = recommendationsHTML;
}

function getSkillRecommendations(skill, lang = 'en') {
    const recommendations = {
        "Web Fundamentals": {
            en: "Focus on understanding URLs, HTTP protocols, and basic web concepts. Practice with browser developer tools.",
            hi: "URL, HTTP प्रोटोकॉल और बुनियादी वेब अवधारणाओं को समझने पर ध्यान दें। ब्राउज़र डेवलपर टूल के साथ अभ्यास करें।"
        },
        "Cybersecurity": {
            en: "Learn about secure connections (HTTPS), password security, and common online threats. Consider cybersecurity courses.",
            hi: "सुरक्षित कनेक्शन (HTTPS), पासवर्ड सुरक्षा और सामान्य ऑनलाइन खतरों के बारे में जानें। साइबर सुरक्षा पाठ्यक्रमों पर विचार करें।"
        }
    };
    
    const recommendation = recommendations[skill];
    if (recommendation) {
        return recommendation[lang] || recommendation.en;
    }
    return lang === 'hi' ? "अभ्यास और अध्ययन के माध्यम से इस क्षेत्र पर ध्यान दें।" : "Focus on this area through practice and study.";
}

function getDifficultyRecommendations(difficulty, lang = 'en') {
    const recommendations = {
        "Basic": {
            en: "Start with fundamental concepts and build a strong foundation before moving to advanced topics.",
            hi: "उन्नत विषयों पर जाने से पहले बुनियादी अवधारणाओं से शुरू करें और एक मजबूत आधार बनाएं।"
        },
        "Intermediate": {
            en: "Practice with real-world scenarios and hands-on exercises to strengthen your understanding.",
            hi: "अपनी समझ को मजबूत करने के लिए वास्तविक दुनिया के परिदृश्यों और हाथों-हाथ अभ्यास के साथ अभ्यास करें।"
        }
    };
    
    const recommendation = recommendations[difficulty];
    if (recommendation) {
        return recommendation[lang] || recommendation.en;
    }
    return lang === 'hi' ? "लक्षित अभ्यास के माध्यम से इस कठिनाई स्तर पर ध्यान दें।" : "Focus on this difficulty level through targeted practice.";
}

function getOverallRecommendations(overallScore, lang = 'en') {
    if (lang === 'hi') {
        if (overallScore >= 90) {
            return "उत्कृष्ट प्रदर्शन! अपनी विशेषज्ञता को और बढ़ाने के लिए उन्नत विषयों और विशेष प्रमाणपत्रों पर विचार करें।";
        } else if (overallScore >= 70) {
            return "अच्छी नींव! अपने कमजोर क्षेत्रों पर ध्यान दें और अपने कौशल को मजबूत करने के लिए मध्यम स्तर के पाठ्यक्रमों पर विचार करें।";
        } else if (overallScore >= 50) {
            return "आपकी बुनियादी समझ है। बुनियादी अवधारणाओं पर ध्यान दें और मजबूत आधार बनाने के लिए शुरुआती-अनुकूल पाठ्यक्रमों पर विचार करें।";
        } else {
            return "बुनियादी डिजिटल साक्षरता पाठ्यक्रमों से शुरू करें और धीरे-धीरे अपना ज्ञान बनाएं। ऑनलाइन संसाधनों और ट्यूटोरियल से मदद लेने में संकोच न करें।";
        }
    } else {
        if (overallScore >= 90) {
            return "Excellent performance! Consider advanced topics and specialized certifications to further enhance your expertise.";
        } else if (overallScore >= 70) {
            return "Good foundation! Focus on your weak areas and consider intermediate-level courses to strengthen your skills.";
        } else if (overallScore >= 50) {
            return "You have a basic understanding. Focus on fundamental concepts and consider beginner-friendly courses to build a stronger foundation.";
        } else {
            return "Start with basic digital literacy courses and gradually build your knowledge. Don't hesitate to seek help from online resources and tutorials.";
        }
    }
}

function resetQuiz() {
    currentQ = 0;
    score = 0;
    userAnswers = [];
    skillPerformance = {};
    window.currentQuestionIndex = currentQ;
    quizStartTime = null;
}

// Initialize on page load
window.addEventListener('load', async function() {
    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    document.getElementById('language-select').value = savedLanguage;
    currentLanguage = savedLanguage;
    
    // Load current user ID if exists
    currentUserId = localStorage.getItem('currentUserId');
    
    // Load questions for the current language
    await fetchQuestions(currentLanguage);
});
