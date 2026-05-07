# 🤖 Groq AI Chatbot

Groq API aur Streamlit se bana hua fast AI chatbot.

## ⚡ Features
- Bilkul FREE (Groq API)
- Multiple AI models
- Chat history
- Adjustable personality
- Token usage tracker

## 🚀 Setup

### 1. Libraries install karo
```bash
pip install -r requirements.txt
```

### 2. API Key setup karo
```bash
# .env file banao
cp .env.example .env
# Ab .env file kholo aur apni Groq API key daalo
```

### 3. Groq API Key kahan se milegi?
1. console.groq.com pe jao
2. Free account banao
3. API Keys section mein jao
4. "Create API Key" pe click karo
5. Key copy karo aur .env mein daalo

### 4. Chatbot run karo
```bash
streamlit run app.py
```

Browser mein khul jayega: http://localhost:8501

## 📦 Project Structure
```
groq-chatbot/
├── app.py              ← Main chatbot code
├── .env                ← API key (private - share mat karna)
├── .env.example        ← Template (share karna safe hai)
├── requirements.txt    ← Libraries
└── README.md           ← Yeh file
```

## 🌐 Free Deployment (Streamlit Cloud)
1. GitHub pe upload karo
2. share.streamlit.io pe jao
3. Repo connect karo
4. GROQ_API_KEY environment variable mein daalo
5. Deploy! ✅
