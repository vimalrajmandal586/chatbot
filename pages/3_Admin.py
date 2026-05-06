import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="Admin - Vimal AI",
    page_icon="👑",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    
    .admin-header {
        background: linear-gradient(90deg, #7c3aed, #3b82f6);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
    }
    
    .metric-card {
        background: rgba(124, 58, 237, 0.1);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Admin Password Protection
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
            <div style="text-align: center; padding: 50px 0;">
                <h1>👑 Admin Login</h1>
                <p style="color: #94a3b8;">Only Vimal Mandal can access this page</p>
            </div>
        """, unsafe_allow_html=True)

        password = st.text_input("🔐 Admin Password", type="password")
        if st.button("Login as Admin", use_container_width=True):
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

    # Logout
    if st.button("🚪 Logout Admin"):
        st.session_state.admin_logged_in = False
        st.rerun()

    # Fetch all users from Firebase
    try:
        users_ref = db.collection("users").stream()
        users_list = []
        for user in users_ref:
            users_list.append(user.to_dict())

        total_users = len(users_list)
        total_messages = sum([u.get("total_messages", 0) for u in users_list])

        # Top Metrics
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
            st.metric("📈 Avg Messages/User", avg_messages)

        st.markdown("---")

        # Users Table
        st.markdown("### 👥 All Users")
        if users_list:
            df = pd.DataFrame(users_list)
            df = df[["name", "email", "total_messages", "first_login", "last_active"]]
            df.columns = ["Name", "Gmail", "Messages", "First Login", "Last Active"]
            st.dataframe(df, use_container_width=True)

            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download User Data",
                csv,
                "vimal_ai_users.csv",
                "text/csv"
            )
        else:
            st.info("No users yet. Share your chatbot link!")

        st.markdown("---")

        # Chart - Messages per User
        if users_list and total_messages > 0:
            st.markdown("### 📊 Messages Per User")
            df_chart = pd.DataFrame(users_list)
            fig = px.bar(
                df_chart,
                x="name",
                y="total_messages",
                color="total_messages",
                color_continuous_scale="Viridis",
                title="Messages per User"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # View Individual Chat History
        st.markdown("### 💬 View User Chat History")
        if users_list:
            user_emails = [u["email"] for u in users_list]
            selected_user = st.selectbox("Select User", user_emails)

            if selected_user and st.button("📖 View Chat History"):
                chat_ref = db.collection("chats").document(selected_user).collection("messages")
                chats = chat_ref.order_by("timestamp").stream()

                chat_list = []
                for chat in chats:
                    chat_list.append(chat.to_dict())

                if chat_list:
                    st.markdown(f"**Chat history for: {selected_user}**")
                    for chat in chat_list:
                        role = "🧑 User" if chat["role"] == "user" else "🤖 AI"
                        st.markdown(f"**{role}:** {chat['content']}")
                        st.markdown(f"*{chat.get('timestamp', '')}*")
                        st.markdown("---")
                else:
                    st.info("No chat history for this user")

        st.markdown("---")

        # Upload Your Photo from Admin Panel
        st.markdown("### 🖼️ Update Your Profile Photo")
        uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            with open("assets/photo.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("✅ Photo updated successfully! Refresh the main page to see it.")

    except Exception as e:
        st.error(f"Database error: {str(e)}")
        st.info("Make sure Firebase is properly configured in secrets.toml")

# Main Logic
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if st.session_state.admin_logged_in:
    admin_dashboard()
else:
    admin_login()
