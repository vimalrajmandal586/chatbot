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

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    
    .chat-header {
        background: linear-gradient(90deg, #7c3aed, #00f5ff);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        color: white;
    }
    
    .user-badge {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 5px 15px;
        color: white;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .login-container {
        text-align: center;
        padding: 50px 20px;
    }
    
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    
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
    st.markdown("""
        <div class="login-container">
            <h1>🔐 Login to Continue</h1>
            <p style="color: #94a3b8;">Enter your Gmail to access the AI Chatbot</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("📧 Enter your Gmail ID", placeholder="yourname@gmail.com")
        name = st.text_input("👤 Enter your Name", placeholder="Your Full Name")

        if st.button("🚀 Login & Start Chatting", use_container_width=True, type="primary"):
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
                        user_ref.update({
                            "last_active": datetime.now().isoformat()
                        })
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

    # Header
    st.markdown(f"""
        <div class="chat-header">
            <h2>💬 Vimal AI Chatbot</h2>
            <div class="user-badge">👤 {name} | {email}</div>
        </div>
    """, unsafe_allow_html=True)

    # Top Buttons
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        if st.button("🆕 New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_loaded = False
            st.rerun()
   with col2:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.logged_in = False
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

    # Initialize Groq
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    # System Prompt
    system_prompt = f"""You are an expert AI assistant built by Vimal Mandal as a personal AI project.
    
    Your expertise covers:
    - Artificial Intelligence and Machine Learning
    - Deep Learning and Neural Networks
    - Computer Science and Programming
    - Data Science and Analytics
    - Web Development (Frontend & Backend)
    - Problem Solving and Logical Reasoning
    - Mathematics and Statistics
    - General Knowledge and Research
    - Any topic the user asks about
    
    The user talking to you is: {name} ({email})
    
    Your personality:
    - You are the mastermind of all fields
    - You are highly intelligent and knowledgeable
    - You explain things clearly with examples
    - You are friendly but professional
    - You remember context from the conversation
    - You give detailed and accurate answers
    - You think step by step for complex questions
    - You never refuse to answer
    
    Always give your absolute best answer."""

    # Load previous chat history from Firebase (ONLY ONCE)
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
            st.toast(f"Could not load history: {e}", icon="⚠️")

        st.session_state.chat_loaded = True

    # Initialize messages if empty
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat Input
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
                full_response = "Sorry, I encountered an error. Please try again."
                response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Save to Firebase
        try:
            chat_ref = db.collection("chats").document(email).collection("messages")

            chat_ref.add({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().isoformat()
            })

            chat_ref.add({
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now().isoformat()
            })

            # Update user stats
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
