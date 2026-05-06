import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pandas as pd
import plotly.express as px

# Page Config - HIDDEN from sidebar
st.set_page_config(
    page_title="Admin - Vimal AI",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Hide sidebar completely
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .admin-header {
        background: linear-gradient(90deg, #7c3aed, #00f5ff);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
    }
    
    .login-box {
        max-width: 400px;
        margin: 50px auto;
        padding: 40px;
        background: rgba(124, 58, 237, 0.05);
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 20px;
        text-align: center;
    }
    
    .login-title {
        font-size: 28px;
        font-weight: 700;
        color: #7c3aed;
        margin-bottom: 10px;
    }
    
    .login-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Admin Password
ADMIN_PASSWORD = "vimal@admin2024"

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

def admin_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="login-box">
                <div class="login-title">👑 Admin Login</div>
                <div class="login-subtitle">Only Vimal Mandal can access this page</div>
            </div>
        """, unsafe_allow_html=True)

        password = st.text_input("🔐 Password", type="password", label_visibility="collapsed", placeholder="Enter Admin Password")
        
        if st.button("Login as Admin", use_container_width=True, type="primary"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("❌ Wrong password!")

def admin_dashboard():
    db = init_firebase()

    # Header
    st.markdown("""
        <div class="admin-header">
            <h1>👑 Vimal AI - Admin Dashboard</h1>
            <p>Complete overview of your AI Chatbot</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()

    try:
        users_ref = db.collection("users").stream()
        users_list = []
        for user in users_ref:
            users_list.append(user.to_dict())

        total_users = len(users_list)
        total_messages = sum([u.get("total_messages", 0) for u in users_list])

        st.markdown("### 📊 Overall Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👥 Total Users", total_users)
        with col2:
            st.metric("💬 Total Messages", total_messages)
        with col3:
            active_today = sum(1 for u in users_list 
                             if u.get("last_active", "")[:10] == datetime.now().strftime("%Y-%m-%d"))
            st.metric("🟢 Active Today", active_today)
        with col4:
            avg_messages = round(total_messages / total_users, 1) if total_users > 0 else 0
            st.metric("📈 Avg Messages", avg_messages)

        st.markdown("---")

        st.markdown("### 👥 All Users")
        if users_list:
            df = pd.DataFrame(users_list)
            display_df = df[["name", "email", "total_messages", "first_login", "last_active"]].copy()
            display_df.columns = ["Name", "Gmail", "Messages", "First Login", "Last Active"]
            st.dataframe(display_df, use_container_width=True)

            csv = display_df.to_csv(index=False)
            st.download_button("📥 Download User Data", csv, "users.csv", "text/csv")
        else:
            st.info("No users yet.")

        st.markdown("---")

        if users_list and total_messages > 0:
            st.markdown("### 📊 Messages Per User")
            df_chart = pd.DataFrame(users_list)
            fig = px.bar(df_chart, x="name", y="total_messages",
                         color="total_messages", color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.markdown("### 💬 View User Chat History")
        if users_list:
            user_emails = [u["email"] for u in users_list]
            selected_user = st.selectbox("Select User", user_emails)

            if selected_user and st.button("📖 View Chat History"):
                chat_ref = db.collection("chats").document(selected_user).collection("messages")
                chats = chat_ref.order_by("timestamp").stream()

                chat_list = [chat.to_dict() for chat in chats]

                if chat_list:
                    st.markdown(f"**Chat history for: {selected_user}**")
                    for chat in chat_list:
                        role = "🧑 User" if chat["role"] == "user" else "🤖 AI"
                        with st.expander(f"{role}: {chat['content'][:80]}..."):
                            st.markdown(chat['content'])
                            st.caption(chat.get('timestamp', ''))
                else:
                    st.info("No chat history for this user")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Main Logic
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if st.session_state.admin_logged_in:
    admin_dashboard()
else:
    admin_login()
