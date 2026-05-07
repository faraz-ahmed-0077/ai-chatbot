import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# ─── Load API Key ───────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY nahi mili! .env file check karo.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }

    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 8px;
    }

    /* Input box */
    .stChatInputContainer {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 12px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.85;
    }

    /* Title */
    h1 {
        background: linear-gradient(90deg, #667eea, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    /* Select box */
    .stSelectbox label {
        color: #a0a0c0 !important;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Settings ────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.divider()

    # Model Selection
    model = st.selectbox(
        "🧠 AI Model Chunno",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ],
        index=0
    )

    # System Prompt
    st.markdown("### 🎭 Chatbot Personality")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, friendly, and knowledgeable AI assistant. Answer clearly and concisely in the language the user is speaking.",
        height=130,
        label_visibility="collapsed"
    )

    # Temperature
    temperature = st.slider("🌡️ Creativity Level", 0.0, 1.0, 0.7, 0.1)

    # Max Tokens
    max_tokens = st.slider("📝 Max Response Length", 256, 4096, 1024, 256)

    st.divider()

    # Clear Chat
    if st.button("🗑️ Chat Clear Karo"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**Model Info:**")
    st.caption(f"Using: `{model}`")
    st.caption(f"Messages: {len(st.session_state.get('messages', []))}")

    st.divider()
    st.markdown(
        "<div style='color:#666; font-size:0.75rem; text-align:center;'>"
        "Powered by Groq ⚡ & LLaMA 3<br>Built with ❤️ in Python"
        "</div>",
        unsafe_allow_html=True
    )

# ─── Main Chat Area ──────────────────────────────────────────────
st.title("🤖 AI Assistant")
st.caption("Groq API | Fast • Free • Powerful")
st.divider()

# Chat history init
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("👋 **Assalam o Alaikum!** Main aapka AI Assistant hun. Kuch bhi pocho — main hamesha madad ke liye haazir hun! 🚀")

# Show existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── User Input ──────────────────────────────────────────────────
if user_input := st.chat_input("Kuch bhi pocho..."):

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("⚡ Soch raha hun..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                reply = response.choices[0].message.content

                st.markdown(reply)

                # Token usage
                usage = response.usage
                st.caption(
                    f"⚡ Tokens used: {usage.total_tokens} "
                    f"(prompt: {usage.prompt_tokens}, "
                    f"response: {usage.completion_tokens})"
                )

            except Exception as e:
                reply = f"❌ Error: {str(e)}"
                st.error(reply)

    # Save assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
