"""
Dark mode theme management for DocQuery
"""

import streamlit as st

def apply_dark_mode():
    """Apply improved dark mode CSS to the app"""
    
    dark_css = """
    <style>
        /* Force dark background on EVERYTHING - including Streamlit's native theme */
        :root {
            --primary-color: #00ff88;
            --background-color: #0a0a0a;
            --secondary-background-color: #0a0a0a;
            --text-color: #e0e0e0;
            --font-color: #e0e0e0;
        }
        
        /* Target ALL possible containers */
        .stApp, .stApp > header, .main, .block-container,
        .stAppViewContainer, .stAppViewBlockContainer, section.main,
        .stMainBlockContainer, .stMain,
        div[data-testid="stVerticalBlock"],
        div[data-testid="stChatInput"],
        div[data-testid="stChatInput"] > div,
        div[class*="st-emotion-cache"],
        div[class*="css-"] {
            background-color: #0a0a0a !important;
        }
        
        /* Fix chat input area */
        .stChatInputContainer, .stChatInputContainer > div,
        div[data-testid="stChatInput"] textarea {
            background-color: #0a0a0a !important;
        }
        
        /* Fix footer */
        footer, .stFooter {
            background-color: #0a0a0a !important;
        }
        
        /* Fix the main content panel */
        .stMainBlockContainer {
            background-color: #0a0a0a !important;
        }
        
        /* Chat messages */
        .stChatMessage {
            background-color: #1a1a1a !important;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        
        /* User message */
        .stChatMessage [data-testid="stChatMessageContent"] {
            background-color: #2a2a3e !important;
            color: white !important;
        }
        
        /* Assistant message */
        .stChatMessage [data-testid="stChatMessageContent"]:has(.assistant) {
            background-color: #1e2a1e !important;
        }
        
        /* Main header */
        .main-header {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 0.5rem;
            color: white;
            margin-bottom: 2rem;
        }
        
        /* Answer box */
        .answer-box {
            background-color: #1e2a1e;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #00ff88;
            margin: 0.5rem 0;
            color: #e0e0e0;
        }
        
        .answer-box strong {
            color: #00ff88;
        }
        
        /* Source card */
        .source-card {
            background-color: #1a1a2e;
            padding: 0.8rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border-left: 3px solid #00ff88;
            color: #c0c0c0;
        }
        
        .source-card strong {
            color: #00ff88;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
            background-color: #0a0a0f !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #e0e0e0 !important;
        }
        
        /* Text input */
        .stTextInput input, 
        .stTextArea textarea,
        .stChatInput textarea {
            background-color: #2a2a2a !important;
            color: white !important;
            border: 1px solid #444 !important;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #2a2a3e !important;
            color: white !important;
            border: 1px solid #444 !important;
        }
        
        .stButton button:hover {
            background-color: #3a3a4e !important;
            border-color: #00ff88 !important;
        }
        
        /* Primary button */
        .stButton button[data-testid="baseButton-primary"] {
            background-color: #00ff88 !important;
            color: #0a0a0a !important;
        }
        
        /* Success message */
        .stSuccess {
            background-color: #1a3a2a !important;
            color: #00ff88 !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #1a1a2e !important;
            color: white !important;
            border-radius: 0.5rem !important;
        }
        
        .streamlit-expanderContent {
            background-color: #0a0a0a !important;
        }
        
        /* Code blocks */
        code {
            background-color: #2a2a3e !important;
            color: #00ff88 !important;
        }
        
        /* Divider */
        hr {
            border-color: #333 !important;
        }
        
        /* File uploader */
        [data-testid="stFileUploader"] {
            background-color: #1a1a2e !important;
            border: 1px dashed #444 !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            background-color: #1a1a1a !important;
        }
        
        ::-webkit-scrollbar-thumb {
            background-color: #00ff88 !important;
            border-radius: 10px !important;
        }
        
        /* Remove all white backgrounds */
        .stAlert, .stInfo, .stWarning, .stError {
            background-color: transparent !important;
        }
        
        /* Make all text readable */
        p, li, span, label, .stMarkdown, div, .stText {
            color: #e0e0e0 !important;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
    </style>
    """
    
    return dark_css


def apply_light_mode():
    """Apply light mode CSS to the app"""
    
    light_css = """
    <style>
        .stApp {
            background-color: #ffffff !important;
        }
        
        .main-header {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 0.5rem;
            color: white;
            margin-bottom: 2rem;
        }
        
        .answer-box {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #28a745;
            margin: 0.5rem 0;
        }
        
        .source-card {
            background-color: #f8f9fa;
            padding: 0.8rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border-left: 3px solid #007bff;
        }
        
        [data-testid="stSidebar"] {
            background-color: #f0f2f6 !important;
        }
    </style>
    """
    
    return light_css


def get_theme_toggle():
    """Create theme toggle button in sidebar and apply theme"""
    
    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    # Create toggle in sidebar
    st.sidebar.subheader("🎨 Appearance")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("☀️ Light", use_container_width=True, key="light_theme_btn"):
            st.session_state.theme = "light"
            st.rerun()
    with col2:
        if st.button("🌙 Dark", use_container_width=True, key="dark_theme_btn"):
            st.session_state.theme = "dark"
            st.rerun()
    
    # Apply selected theme with a unique key to force refresh
    if st.session_state.theme == "dark":
        st.markdown(apply_dark_mode(), unsafe_allow_html=True)
        return "dark"
    else:
        st.markdown(apply_light_mode(), unsafe_allow_html=True)
        return "light"


def get_current_theme():
    """Get current theme"""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    return st.session_state.theme