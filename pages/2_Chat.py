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

# Custom CSS - FIXED
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
    
    /* Animated Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(124, 58, 237, 0.3),
            rgba(0, 0, 0, 0.7),
            rgba(0, 245, 255, 0.2));
        z-index: 0;
        animation: gradientShift 10s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { 
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(0, 0, 0, 0.7), rgba(0, 245, 255, 0.2)); 
        }
        50% { 
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.3), rgba(0, 0, 0, 0.7), rgba(255, 0, 168, 0.2)); 
        }
    }
    
    .main .block-container {
        position: relative;
        z-index: 10;
        padding-top: 50px !important;
    }
    
    /* Login Heading */
    .login-heading {
        font-family: 'Instrument Serif', serif;
        font-size: 56px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        letter-spacing: -0.02em;
        line-height: 1;
    }
    
    .login-subtitle {
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    /* Chat Header */
    .chat-header {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 20px 30px;
        border-radius: 25px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .chat-title {
        font-family: 'Instrument Serif', serif;
        font-size: 32px;
        color: white;
        margin-bottom: 8px;
    }
    
    .user-badge {
        background: rgba(124, 58, 237, 0.3);
        border: 1px solid rgba(124, 58, 237, 0.6);
        border-radius: 20px;
        padding: 6px 16px;
        color: #fff;
        font-size: 13px;
        display: inline-block;
    }
    
    /* INPUT BOXES - WHITE BACKGROUND, BLACK TEXT */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 50px !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        padding: 15px 25px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        caret-color: #000000 !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 1) !important;
        border: 2px solid #7c3aed !important;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.5) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.5) !important;
        font-weight: 400 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 50px !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 12px 30px !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4);
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        color: white !important;
    }
    
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div {
        color: white !important;
    }
    
    /* Chat input - WHITE BACKGROUND, BLACK TEXT */
    [data-testid="stChatInput"] textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: rgba(0, 0, 0, 0.5) !important;
    }
    
    /* All text white */
    .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    /* HIDE ANCHOR LINKS NEXT TO HEADINGS */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    
    .stMarkdown h1 a,
    .stMarkdown h2 a,
    .stMarkdown h3 a {
        display: none !important;
    }
    
    /* Hide any link icons */
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    
    </style>
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
        
        email = st.text_input("Email", placeholder="Enter your Gmail", label_visibility="collapsed", key="email_input")
        name = st.text_input("Name", placeholder="Enter your Name", label_visibility="collapsed", key="name_input")

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
