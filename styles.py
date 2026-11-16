import streamlit as st

def apply_css(theme="Light", is_login=False):
    # Professional Sage & Gray Palette with Bold Black/White Borders
    if theme == "Light":
        bg_color = "#dfe8e1"
        card_bg = "#FFFFFF"
        text_primary = "#000000"
        text_secondary = "#111827"
        accent = "#4F46E5"
        border_color = "#000000"
        chat_bg = "#FFFFFF"
    else:
        bg_color = "#0F172A"       # Dark Slate
        card_bg = "#1E293B"       # Slate 800
        text_primary = "#FFFFFF"
        text_secondary = "#94A3B8"
        accent = "#818CF8"
        border_color = "#FFFFFF"   # White borders for dark mode
        chat_bg = "#1E293B"

    css_lines = [
        "<style>",
        "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');",
        
        "/* Global Background */",
        f'[data-testid="stAppViewContainer"] {{ background-color: {bg_color} !important; font-family: "Inter", sans-serif; }}',
        f'[data-testid="stHeader"] {{ background: transparent !important; }}',
        "footer { visibility: hidden; }",
        
        "/* Main Containers with Bold 2px Border */",
        f'[data-testid="stVerticalBlockBorderWrapper"] {{ background: {card_bg} !important; border: 2px solid {border_color} !important; border-radius: 12px !important; padding: 2rem !important; margin-bottom: 1.5rem !important; }}',
        f'[data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"] {{ border: 2px solid {border_color} !important; }}',
        
        "/* Theme Toggle (Selectbox) - Deep Fix */",
        f'[data-testid="stSelectbox"] div[data-baseweb="select"] {{ background-color: {bg_color} !important; border: 2px solid {border_color} !important; border-radius: 8px !important; }}',
        f'[data-testid="stSelectbox"] div[data-baseweb="select"] * {{ color: {text_primary} !important; background-color: transparent !important; }}',
        
        "/* Dropdown List Fix (Selectbox popover) */",
        f'div[data-baseweb="popover"] ul {{ background-color: {card_bg} !important; border: 2px solid {border_color} !important; }}',
        f'div[data-baseweb="popover"] li {{ background-color: transparent !important; color: {text_primary} !important; }}',
        f'div[data-baseweb="popover"] li:hover {{ background-color: {bg_color} !important; }}',
        
        "/* Inputs & Fields (Body Colored) */",
        f'.stTextInput input, .stTextArea textarea {{ background: {bg_color} !important; border: 2px solid {border_color} !important; border-radius: 8px !important; color: {text_primary} !important; font-weight: 600 !important; caret-color: {text_primary} !important; }}',
        f'::placeholder {{ color: {text_secondary} !important; opacity: 0.6 !important; }}',
        
        "/* Chat Input (Body Colored) */",
        f'[data-testid="stChatInput"] textarea {{ background-color: {bg_color} !important; border: 2px solid {border_color} !important; border-radius: 8px !important; color: {text_primary} !important; font-weight: 500 !important; caret-color: {text_primary} !important; }}',
        f'[data-testid="stChatInput"] textarea::placeholder {{ color: {text_secondary} !important; }}',
        f'[data-testid="stChatInput"] div {{ background-color: transparent !important; }}',
        
        "/* Buttons */",
        f'.stButton button {{ border: 2px solid {border_color} !important; border-radius: 8px !important; font-weight: 800 !important; transition: all 0.2s ease !important; background-color: transparent !important; color: {text_primary} !important; }}',
        f'.stButton button[kind="primary"] {{ background-color: {accent} !important; color: #FFFFFF !important; border: none !important; }}',
        f'.stDownloadButton button {{ background-color: {bg_color} !important; color: {text_primary} !important; border: 2px solid {border_color} !important; }}',
        
        "/* Sidebar */",
        f'[data-testid="stSidebar"] {{ background-color: {bg_color} !important; border-right: 2px solid {border_color} !important; }}',
        f'[data-testid="stSidebar"] * {{ color: {text_primary} !important; }}',
        
        "/* Expanders */",
        f'.stExpander {{ background-color: {bg_color} !important; border: 2px solid {border_color} !important; border-radius: 8px !important; }}',
        f'.stExpander * {{ background-color: transparent !important; color: {text_primary} !important; }}',
        
        "/* Chat Assistant & Bubbles */",
        f'[data-testid="stChatMessageContainer"] {{ border: 2px solid {border_color} !important; border-radius: 12px !important; background: {chat_bg} !important; padding: 10px !important; }}',
        f'[data-testid="stChatMessage"] {{ border: 2px solid {border_color} !important; border-radius: 12px !important; background: {card_bg} !important; color: {text_primary} !important; }}',
        f'[data-testid="stChatMessage"] * {{ color: {text_primary} !important; }}',
        
        "/* Text Colors Global */",
        f'h1, h2, h3, h4, h5, h6, p, span, label, li, .stMarkdown p {{ color: {text_primary} !important; }}',
        
        "/* Intelligence Report Card */",
        f'.custom-card {{ background: rgba(255,255,255,0.05); border: 2px solid {border_color}; border-radius: 8px; padding: 1.5rem; color: {text_primary} !important; font-weight: 600; }}',
        f'.custom-card * {{ color: {text_primary} !important; }}',
        
        "/* Login Title - Explicit Centering */",
        f'.login-title {{ font-size: 3.5rem !important; font-weight: 900 !important; color: {text_primary} !important; text-align: center !important; width: 100% !important; display: block !important; }}'
    ]

    css_lines.append("</style>")
    st.markdown("".join(css_lines), unsafe_allow_html=True)
