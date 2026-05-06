import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(
    page_title="Vimal Mandal - 3D AI Creator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    [data-testid="stSidebar"] {display: none;}
    .stApp {background: #0C0C0C;}
    .main .block-container {padding: 0 !important; max-width: 100% !important;}
    .stApp > header {display: none;}
    </style>
""", unsafe_allow_html=True)

# Hero HTML
hero_html = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700;800;900&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Kanit', sans-serif;
}

body, html {
    background: #0C0C0C;
    color: white;
    overflow-x: hidden;
}

.hero-container {
    min-height: 100vh;
    background: #0C0C0C;
    display: flex;
    flex-direction: column;
    overflow-x: clip;
    position: relative;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    padding: 30px 40px;
    color: #D7E2EA;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500;
    font-size: 1.2rem;
    z-index: 100;
}

.navbar a {
    color: #D7E2EA;
    text-decoration: none;
    transition: opacity 0.2s;
    cursor: pointer;
}

.navbar a:hover {
    opacity: 0.7;
}

/* Hero Heading */
.hero-heading {
    font-size: 17vw;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: -0.05em;
    line-height: 0.9;
    text-align: center;
    background: linear-gradient(180deg, #646973 0%, #BBCCD7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: -30px;
    white-space: nowrap;
    animation: fadeUp 1s ease forwards;
    opacity: 0;
    animation-delay: 0.3s;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Portrait Image */
.portrait {
    position: absolute;
    left: 50%;
    bottom: 0;
    transform: translateX(-50%);
    width: 480px;
    z-index: 10;
    border-radius: 30px;
    transition: transform 0.4s ease-out;
    animation: fadeUp 1s ease forwards;
    opacity: 0;
    animation-delay: 0.6s;
}

.portrait:hover {
    transform: translateX(-50%) scale(1.05);
}

/* Bottom Bar */
.bottom-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0 40px 50px 40px;
    margin-top: auto;
    position: relative;
    z-index: 20;
}

.bottom-text {
    color: #D7E2EA;
    font-weight: 300;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 1.2rem;
    max-width: 280px;
    line-height: 1.3;
    animation: fadeUp 1s ease forwards;
    opacity: 0;
    animation-delay: 0.9s;
}

/* Contact Button */
.contact-btn {
    background: linear-gradient(123deg, #18011F 7%, #B600A8 37%, #7621B0 72%, #BE4C00 100%);
    color: white;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: 500;
    padding: 16px 48px;
    border-radius: 50px;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    box-shadow: 
        inset 0 4px 4px rgba(181, 1, 167, 0.25),
        inset 4px 4px 12px #7721B1,
        0 0 0 2px white;
    outline-offset: -3px;
    font-family: 'Kanit', sans-serif;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.3s ease;
    animation: fadeUp 1s ease forwards;
    opacity: 0;
    animation-delay: 0.9s;
}

.contact-btn:hover {
    transform: scale(1.05);
}

/* About Section */
.about-section {
    min-height: 100vh;
    padding: 100px 40px;
    background: #0C0C0C;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
    position: relative;
}

.about-heading {
    font-size: clamp(3rem, 12vw, 160px);
    font-weight: 900;
    text-transform: uppercase;
    background: linear-gradient(180deg, #646973 0%, #BBCCD7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    letter-spacing: -0.03em;
    text-align: center;
}

.about-text {
    color: #D7E2EA;
    font-weight: 500;
    text-align: center;
    line-height: 1.6;
    max-width: 600px;
    font-size: clamp(1rem, 2vw, 1.4rem);
}

/* Services Section */
.services-section {
    background: #FFFFFF;
    border-top-left-radius: 60px;
    border-top-right-radius: 60px;
    padding: 100px 40px;
    color: #0C0C0C;
}

.services-heading {
    font-size: clamp(3rem, 12vw, 160px);
    font-weight: 900;
    text-transform: uppercase;
    color: #0C0C0C;
    text-align: center;
    margin-bottom: 80px;
    line-height: 1;
}

.service-list {
    max-width: 1200px;
    margin: 0 auto;
}

.service-item {
    display: flex;
    align-items: flex-start;
    gap: 40px;
    padding: 40px 0;
    border-bottom: 1px solid rgba(12, 12, 12, 0.15);
}

.service-num {
    font-size: clamp(3rem, 8vw, 100px);
    font-weight: 900;
    color: #0C0C0C;
    min-width: 150px;
}

.service-content {
    flex: 1;
}

.service-name {
    font-size: clamp(1.2rem, 2.5vw, 2rem);
    font-weight: 500;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.service-desc {
    font-size: clamp(0.9rem, 1.5vw, 1.2rem);
    font-weight: 300;
    line-height: 1.6;
    opacity: 0.6;
    max-width: 700px;
}

/* Marquee */
.marquee-section {
    padding: 60px 0;
    background: #0C0C0C;
    overflow: hidden;
}

.marquee {
    display: flex;
    gap: 20px;
    animation: scroll 30s linear infinite;
    width: max-content;
}

.marquee-2 {
    animation: scroll-reverse 25s linear infinite;
    margin-top: 20px;
}

@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

@keyframes scroll-reverse {
    0% { transform: translateX(-50%); }
    100% { transform: translateX(0); }
}

.marquee-tile {
    width: 380px;
    height: 240px;
    border-radius: 20px;
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    font-weight: 600;
    flex-shrink: 0;
    border: 1px solid rgba(255,255,255,0.1);
}

.marquee-tile-1 { background: linear-gradient(135deg, #667eea, #764ba2); }
.marquee-tile-2 { background: linear-gradient(135deg, #f093fb, #f5576c); }
.marquee-tile-3 { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.marquee-tile-4 { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.marquee-tile-5 { background: linear-gradient(135deg, #fa709a, #fee140); }
.marquee-tile-6 { background: linear-gradient(135deg, #30cfd0, #330867); }

</style>
</head>
<body>

<!-- HERO SECTION -->
<div class="hero-container">
    <nav class="navbar">
        <a>About</a>
        <a>Skills</a>
        <a>Projects</a>
        <a>Contact</a>
    </nav>
    
    <h1 class="hero-heading">Hi, i&apos;m vimal</h1>
    
    <img class="portrait" 
         src="https://i.ibb.co/Vcj9MQYr/Whats-App-Image-2026-04-05-at-8-49-04-PM.jpg" 
         alt="Vimal Mandal"/>
    
    <div class="bottom-bar">
        <p class="bottom-text">An AI creator driven by building intelligent and unforgettable projects</p>
        <button class="contact-btn">Get In Touch</button>
    </div>
</div>

<!-- MARQUEE -->
<div class="marquee-section">
    <div class="marquee">
        <div class="marquee-tile marquee-tile-1">🤖 AI Chatbot</div>
        <div class="marquee-tile marquee-tile-2">🧠 Machine Learning</div>
        <div class="marquee-tile marquee-tile-3">⚡ Llama 3.3 70B</div>
        <div class="marquee-tile marquee-tile-4">💬 Smart Chat</div>
        <div class="marquee-tile marquee-tile-5">🚀 Fast Response</div>
        <div class="marquee-tile marquee-tile-6">🔒 Secure</div>
        <div class="marquee-tile marquee-tile-1">🤖 AI Chatbot</div>
        <div class="marquee-tile marquee-tile-2">🧠 Machine Learning</div>
        <div class="marquee-tile marquee-tile-3">⚡ Llama 3.3 70B</div>
        <div class="marquee-tile marquee-tile-4">💬 Smart Chat</div>
        <div class="marquee-tile marquee-tile-5">🚀 Fast Response</div>
        <div class="marquee-tile marquee-tile-6">🔒 Secure</div>
    </div>
    <div class="marquee marquee-2">
        <div class="marquee-tile marquee-tile-6">🌟 Powerful</div>
        <div class="marquee-tile marquee-tile-5">📊 Analytics</div>
        <div class="marquee-tile marquee-tile-4">🎯 Accurate</div>
        <div class="marquee-tile marquee-tile-3">💡 Innovative</div>
        <div class="marquee-tile marquee-tile-2">🔥 Modern</div>
        <div class="marquee-tile marquee-tile-1">⭐ Premium</div>
        <div class="marquee-tile marquee-tile-6">🌟 Powerful</div>
        <div class="marquee-tile marquee-tile-5">📊 Analytics</div>
        <div class="marquee-tile marquee-tile-4">🎯 Accurate</div>
        <div class="marquee-tile marquee-tile-3">💡 Innovative</div>
        <div class="marquee-tile marquee-tile-2">🔥 Modern</div>
        <div class="marquee-tile marquee-tile-1">⭐ Premium</div>
    </div>
</div>

<!-- ABOUT SECTION -->
<div class="about-section">
    <h2 class="about-heading">About Me</h2>
    <p class="about-text">
        With a passion for AI and innovation, I built this intelligent chatbot using cutting-edge 
        Llama 3.3 70B model. I focus on creating AI experiences that are powerful, intuitive, and 
        truly helpful. Let's build something incredible together!
    </p>
    <button class="contact-btn">Start Chatting</button>
</div>

<!-- SERVICES SECTION -->
<div class="services-section">
    <h2 class="services-heading">Services</h2>
    <div class="service-list">
        <div class="service-item">
            <div class="service-num">01</div>
            <div class="service-content">
                <div class="service-name">AI Chatbot</div>
                <div class="service-desc">Intelligent conversational AI powered by Llama 3.3 70B model that can answer any question with accuracy and context.</div>
            </div>
        </div>
        <div class="service-item">
            <div class="service-num">02</div>
            <div class="service-content">
                <div class="service-name">Smart Memory</div>
                <div class="service-desc">Advanced memory system that remembers your past conversations and provides contextual responses across sessions.</div>
            </div>
        </div>
        <div class="service-item">
            <div class="service-num">03</div>
            <div class="service-content">
                <div class="service-name">Expert Knowledge</div>
                <div class="service-desc">Domain expertise covering AI, Machine Learning, Programming, Data Science, Mathematics, and general knowledge.</div>
            </div>
        </div>
        <div class="service-item">
            <div class="service-num">04</div>
            <div class="service-content">
                <div class="service-name">Secure Login</div>
                <div class="service-desc">Safe Gmail-based authentication with encrypted user data storage on Firebase cloud database.</div>
            </div>
        </div>
        <div class="service-item">
            <div class="service-num">05</div>
            <div class="service-content">
                <div class="service-name">Lightning Fast</div>
                <div class="service-desc">Powered by Groq's ultra-fast inference engine delivering instant responses with streaming output.</div>
            </div>
        </div>
    </div>
</div>

</body>
</html>
"""

# Render the HTML
components.html(hero_html, height=2400, scrolling=True)

# Floating Start Chat Button (Streamlit native)
st.markdown("""
    <style>
    .stButton > button {
        background: linear-gradient(123deg, #18011F 7%, #B600A8 37%, #7621B0 72%, #BE4C00 100%) !important;
        color: white !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 600 !important;
        padding: 18px 60px !important;
        border-radius: 50px !important;
        border: 2px solid white !important;
        font-size: 18px !important;
        box-shadow: 0 0 40px rgba(181, 1, 167, 0.5);
        font-family: 'Kanit', sans-serif !important;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 60px rgba(181, 1, 167, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 START CHATTING NOW", use_container_width=True):
        st.switch_page("pages/2_Chat.py")
