import streamlit as st
from groq import Groq
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Chat - Vimal AI",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Glass Morphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: #000000;
    }
    
    /* Background Video */
    .video-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .video-bg::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(124, 58, 237, 0.3),
            rgba(0, 0, 0, 0.7),
            rgba(0, 245, 255, 0.2));
        z-index: 1;
        animation: gradientShift 10s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(0, 0, 0, 0.7), rgba(0, 245, 255, 0.2)); }
        50% { background: linear-gradient(135deg, rgba(0, 245, 255, 0.3), rgba(0, 0, 0, 0.7), rgba(255, 0, 168, 0.2)); }
    }
    
    /* Liquid Glass Effect */
    .liquid-glass {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1),
                    0 8px 32px rgba(0, 0, 0, 0.3);
        border-radius: 50px;
        padding: 30px;
    }
    
    /* Login Heading */
    .login-heading {
        font-family: 'Instrument Serif', serif;
        font-size: 64px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        letter-spacing: -0.02em;
        line-height: 1;
    }
    
    .login-subtitle {
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
        font-size: 16px;
        margin-bottom: 40px;
    }
    
    /* Chat Header */
    .chat-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px 30px;
        border-radius: 25px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
    }
    
    .chat-title {
        font-family: 'Instrument Serif', serif;
        font-size: 32px;
        color: white;
        margin-bottom: 8px;
    }
    
    .user-badge {
        background: rgba(124, 58, 237, 0.2);
        border: 1px solid rgba(124, 58, 237, 0.4);
        border-radius: 20px;
        padding: 6px 16px;
        color: #fff;
        font-size: 13px;
        display: inline-block;
    }
    
    /* Streamlit Inputs */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 50px !important;
        color: white !important;
        padding: 15px 25px !important;
        font-size: 16px !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .stTextInput label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 12px 30px !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        backdrop-filter: blur(20px);
    }
    
    /* All text white */
    .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Animated Background
st.markdown("""
    <div class="video-bg"></div>
""", unsafe_allow_html=True)

# Initialize Firebase
def init_firebase():
    if not firebase_admin._apps:
        firebase_config = {
            "type": "service_account",
            "project_id": st.secrets["firebase"]["projectId"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"],
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Login Section
def login_section():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="login-heading">Built for the curious</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Login to start your AI journey with Vimal\'s personalized chatbot</p>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="Enter your Gmail", label_visibility="collapsed")
        name = st.text_input("Name", placeholder="Enter your Name", label_visibility="collapsed")

        if st.button("🚀 Login & Start Chatting", use_container_width=True):
            if email and "@gmail.com" in email and name:
                st.session_state.user_email = email
                st.session_state.user_name = name
                st.session_state.logged_in = True
                st.session_state.messages = []
                st.session_state.chat_loaded = False

                try:
                    db = init_firebase()
                    user_ref = db.collection("users").document(email)
                    user_data = user_ref.get()

                    if not user_data.exists:
                        user_ref.set({
                            "email": email,
                            "name": name,
                            "first_login": datetime.now().isoformat(),
                            "last_active": datetime.now().isoformat(),
                            "total_messages": 0
                        })
                    else:
                        user_ref.update({"last_active": datetime.now().isoformat()})
                except Exception as e:
                    st.warning(f"Database issue: {e}")

                st.rerun()
            else:
                if not email or "@gmail.com" not in email:
                    st.error("❌ Please enter a valid Gmail ID")
                if not name:
                    st.error("❌ Please enter your name")

# Chat Section
def chat_section():
    db = init_firebase()
    email = st.session_state.user_email
    name = st.session_state.user_name

    st.markdown(f"""
        <div class="chat-header">
            <div class="chat-title">💬 Vimal AI</div>
            <div class="user-badge">👤 {name} | {email}</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        if st.button("🆕 New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_loaded = False
            st.rerun()
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.messages = []
            st.session_state.chat_loaded = False
            st.rerun()

    st.markdown("---")

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    system_prompt = f"""You are an expert AI assistant built by Vimal Mandal as a personal AI project.
    
    Your expertise covers:
    - Artificial Intelligence and Machine Learning
    - Deep Learning and Neural Networks
    - Computer Science and Programming
    - Data Science and Analytics
    - Web Development
    - Mathematics and Statistics
    - General Knowledge
    
    User: {name} ({email})
    
    Be intelligent, helpful, and clear. Think step by step. Always give your best answer."""

    if not st.session_state.get("chat_loaded", False):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        try:
            chat_ref = db.collection("chats").document(email).collection("messages")
            past_chats = chat_ref.order_by("timestamp").stream()
            loaded_messages = []
            for chat in past_chats:
                chat_data = chat.to_dict()
                loaded_messages.append({
                    "role": chat_data["role"],
                    "content": chat_data["content"]
                })
            if loaded_messages:
                st.session_state.messages.extend(loaded_messages)
                st.toast(f"📜 Loaded {len(loaded_messages)} previous messages!", icon="✅")
        except Exception as e:
            pass
        st.session_state.chat_loaded = True

    if not st.session_state.messages:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=2048,
                    stream=True,
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                full_response = "Sorry, error occurred. Please try again."

        st.session_state.messages.append({"role": "assistant", "content": full_response})

        try:
            chat_ref = db.collection("chats").document(email).collection("messages")
            chat_ref.add({"role": "user", "content": prompt, "timestamp": datetime.now().isoformat()})
            chat_ref.add({"role": "assistant", "content": full_response, "timestamp": datetime.now().isoformat()})
            user_ref = db.collection("users").document(email)
            user_data = user_ref.get()
            if user_data.exists:
                current_count = user_data.to_dict().get("total_messages", 0)
                user_ref.update({
                    "total_messages": current_count + 1,
                    "last_active": datetime.now().isoformat()
                })
        except Exception as e:
            pass

# Main Logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    chat_section()
else:
    login_section()
