import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(
    page_title="Vimal Mandal - AI Project",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide everything
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    .stApp {background: #000000;}
    .main .block-container {padding: 0 !important; max-width: 100% !important;}
    </style>
""", unsafe_allow_html=True)

# Full Page HTML
page_html = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}

body {
    background: #000;
    overflow-x: hidden;
}

.hero-section {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), 
                url('https://img.freepik.com/premium-photo/woman-standing-top-mountain-illustration-futuristic-world-with-sunset-sky_916191-39663.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    text-align: center;
}

.profile-img {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    border: 4px solid #00f5ff;
    object-fit: cover;
    margin-bottom: 25px;
    box-shadow: 0 0 40px rgba(0, 245, 255, 0.5), 0 0 80px rgba(124, 58, 237, 0.3);
    animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 40px rgba(0, 245, 255, 0.5); }
    50% { box-shadow: 0 0 60px rgba(0, 245, 255, 0.8), 0 0 100px rgba(124, 58, 237, 0.5); }
}

.hero-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 55px;
    font-weight: 900;
    background: linear-gradient(90deg, #00f5ff, #7c3aed, #ff6b6b, #00f5ff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-flow 4s ease infinite;
    margin-bottom: 10px;
}

@keyframes gradient-flow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-subtitle {
    font-size: 20px;
    color: #00f5ff;
    font-weight: 300;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 25px;
}

.hero-desc {
    font-size: 17px;
    color: #c0c0c0;
    max-width: 750px;
    line-height: 1.8;
    margin-bottom: 35px;
}

.stats-container {
    display: flex;
    gap: 50px;
    margin: 25px 0;
    flex-wrap: wrap;
    justify-content: center;
}

.stat-item { text-align: center; }

.stat-number {
    font-family: 'Orbitron', sans-serif;
    font-size: 34px;
    font-weight: 700;
    color: #00f5ff;
}

.stat-label {
    font-size: 13px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.features-container {
    display: flex;
    gap: 20px;
    margin: 35px 0;
    flex-wrap: wrap;
    justify-content: center;
}

.feature-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 245, 255, 0.2);
    border-radius: 20px;
    padding: 25px 20px;
    width: 200px;
    text-align: center;
    transition: all 0.4s ease;
}

.feature-card:hover {
    transform: translateY(-10px);
    border-color: #00f5ff;
    box-shadow: 0 20px 40px rgba(0, 245, 255, 0.2);
}

.feature-icon { font-size: 35px; margin-bottom: 12px; }
.feature-title { font-size: 16px; font-weight: 600; color: #ffffff; margin-bottom: 6px; }
.feature-text { font-size: 13px; color: #94a3b8; line-height: 1.5; }

.footer-text {
    margin-top: 40px;
    color: #475569;
    font-size: 13px;
}

</style>
</head>
<body>

<div class="hero-section">

    <img class="profile-img" 
         src="https://i.ibb.co/Vcj9MQYr/Whats-App-Image-2026-04-05-at-8-49-04-PM.jpg" 
         alt="Vimal Mandal"/>

    <div class="hero-name">VIMAL MANDAL</div>

    <div class="hero-subtitle">AI Developer &#8226; Innovator &#8226; Creator</div>

    <div class="hero-desc">
        Hello! My name is Vimal Mandal. Having just completed my 12th-grade education, 
        I built this website from scratch to showcase my journey in coding, featuring 
        Python-to-web conversions and interactive interfaces. Please explore the projects, 
        have a try, and see how they work firsthand.
    </div>

    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-number">70B</div>
            <div class="stat-label">Parameters</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">&#8734;</div>
            <div class="stat-label">Knowledge</div>
        </div>
    </div>

    <div class="features-container">
        <div class="feature-card">
            <div class="feature-icon">&#129504;</div>
            <div class="feature-title">Smart AI</div>
            <div class="feature-text">Powered by Llama 3.3 70B - World class intelligence</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">&#128172;</div>
            <div class="feature-title">Chat History</div>
            <div class="feature-text">Remembers all your previous conversations</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">&#128274;</div>
            <div class="feature-title">Secure Login</div>
            <div class="feature-text">Login with Gmail - Your data is safe</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">&#9889;</div>
            <div class="feature-title">Lightning Fast</div>
            <div class="feature-text">Instant responses powered by Groq</div>
        </div>
    </div>

    <div class="footer-text">
        &copy; 2024 Vimal Mandal | AI Chatbot Project | Built with &#10084;&#65039;
    </div>

</div>

</body>
</html>
"""

# Render the full HTML page
components.html(page_html, height=900, scrolling=True)

# Start Button
st.markdown("")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 START CHATTING NOW", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Chat.py")
