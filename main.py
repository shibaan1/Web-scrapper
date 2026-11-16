import streamlit as st
import re
import traceback
from view_model import ViewModel
from styles import apply_css

st.set_page_config(page_title="AI Web Scraper", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")

if "vm" not in st.session_state:
    st.session_state.vm = ViewModel()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "url_input" not in st.session_state: st.session_state.url_input = ""
if "prompt_input" not in st.session_state: st.session_state.prompt_input = ""
if "theme" not in st.session_state:
    st.session_state.theme = "Light"


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.chat_history = []
    st.session_state.pop("dom_content", None)
    st.session_state.pop("current_scrape_id", None)


if not st.session_state.logged_in:
    apply_css(theme=st.session_state.theme, is_login=True)
    
    # Theme toggle top right
    tcol1, tcol2 = st.columns([10, 1])
    with tcol2:
        new_theme = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1, label_visibility="collapsed")
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()

    # Login UI
    st.markdown("<h1 class='login-title' style='text-align: center;'>AI Scraper.</h1>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='text-align: center; margin-bottom: 2rem; font-size: 1.1rem;'>Modern web intelligence platform.</p>", unsafe_allow_html=True)
    
    # Center login
    _, lcol, _ = st.columns([1, 1.5, 1])
    with lcol:
        with st.container(border=True):
            tab1, tab2 = st.tabs(["Sign In", "Register"])

            with tab1:
                st.markdown("<br>", unsafe_allow_html=True)
                login_email = st.text_input("Email", key="login_email", placeholder="your@email.com")
                login_password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")

                if st.button("Access Dashboard", type="primary"):
                    success, result = st.session_state.vm.login(login_email, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = result
                        st.rerun()
                    else:
                        st.error(result)

            with tab2:
                st.markdown("<br>", unsafe_allow_html=True)
                signup_name = st.text_input("Full Name", key="signup_name", placeholder="Full Name")
                signup_email = st.text_input("Email Address", key="signup_email", placeholder="name@company.com")
                signup_password = st.text_input("Create Password", type="password", key="signup_password")
                signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

                if st.button("Create Account", type="primary"):
                    success, message = st.session_state.vm.register(signup_name, signup_email, signup_password, signup_confirm)
                    if success:
                        st.success("Account created!")
                    else:
                        st.error(message)

else:
    apply_css(theme=st.session_state.theme, is_login=False)
    
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("<h2 style='margin-bottom:0;'>AI Scraper.</h2>", unsafe_allow_html=True)
        st.caption(f"Authenticated: {st.session_state.user['email']}")
        st.markdown("<br>", unsafe_allow_html=True)
        
        page = st.radio("MENU", ["Dashboard", "History", "Profile"])
        
        st.markdown("<div style='position: fixed; bottom: 30px; width: 240px;'>", unsafe_allow_html=True)
        st.divider()
        new_theme = st.radio("APPEARANCE", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1, horizontal=True)
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()
        
        if st.button("Sign Out", type="secondary", use_container_width=True):
            logout()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    # --- PAGE ROUTING ---
    if page == "Dashboard":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.title("Scrape Hub")
        st.markdown("<p class='text-secondary'>Enter a URL to begin analysis.</p>", unsafe_allow_html=True)
        
        with st.container():
            # If URL input is empty, clear the state to ensure a blank dashboard
            if not st.session_state.url_input:
                st.session_state.pop("dom_content", None)
                st.session_state.pop("extraction_result", None)
                st.session_state.chat_history = []

            with st.form("scrape_form", clear_on_submit=False):
                url_col, btn_col = st.columns([4, 1])
                with url_col:
                    url = st.text_input("Target URL", value=st.session_state.url_input, placeholder="https://example.com", label_visibility="collapsed", key="url_input_widget")
                with btn_col:
                    scrape_clicked = st.form_submit_button("Start Scrape", type="primary", use_container_width=True)
                
                if scrape_clicked:
                    if not url:
                        st.error("URL is required.")
                    else:
                        # TOTAL RESET for new scrape
                        st.session_state.url_input = "" 
                        st.session_state.pop("dom_content", None)
                        st.session_state.pop("extraction_result", None)
                        st.session_state.chat_history = []
                        st.session_state.prompt_input = ""
                        
                        try:
                            with st.spinner("Processing..."):
                                success, result = st.session_state.vm.scrape_site(st.session_state.user["id"], url)
                                
                            if success:
                                st.session_state.url_input = url # Set it back after success
                                st.session_state.current_url = result["url"]
                                st.session_state.dom_content = result["content"]
                                st.session_state.current_scrape_id = result["scrape_id"]
                                st.rerun() # Force refresh to show new data
                            else:
                                st.error(result)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
        if st.session_state.get("dom_content"):
            st.divider()
            
            dash_col1, dash_col2 = st.columns([1, 1], gap="large")
            
            with dash_col1:
                with st.container(border=True):
                    st.subheader("Data Extraction")
                    parse_description = st.text_area(
                        "Extraction Prompt",
                        value=st.session_state.prompt_input,
                        placeholder="What details should I find?",
                        height=100,
                        key="prompt_input_widget"
                    )
                    
                    if st.button("Extract Data", type="primary"):
                        st.session_state.prompt_input = parse_description # Save to state
                        with st.spinner("AI analyzing..."):
                            success, result = st.session_state.vm.extract_data(
                                st.session_state.current_scrape_id,
                                st.session_state.dom_content,
                                parse_description
                            )
                        if success:
                            st.session_state.extraction_result = result
                        else:
                            st.warning(result)

                    if "extraction_result" in st.session_state:
                        st.markdown(f"<div class='custom-card'>{st.session_state.extraction_result}</div>", unsafe_allow_html=True)
                        st.download_button("Download (.txt)", data=st.session_state.extraction_result, file_name="extraction.txt")
                
                with st.expander("Raw Data View"):
                    st.code(st.session_state.dom_content[:1000] + "...", language="html")
                        
            with dash_col2:
                with st.container(border=True):
                    st.subheader("AI Chat Assistant")
                    chat_container = st.container(height=400)
                    with chat_container:
                        if not st.session_state.chat_history:
                            st.info("Ask me about the page content.")
                        for m in st.session_state.chat_history:
                            with st.chat_message(m["role"]):
                                st.markdown(m["content"])
                                
                    q = st.chat_input("Message AI...")
                    if q:
                        st.session_state.chat_history.append({"role": "user", "content": q})
                        with chat_container:
                            with st.chat_message("user"): st.markdown(q)
                            with st.chat_message("assistant"):
                                with st.spinner("Thinking..."):
                                    data = [{"url": st.session_state.current_url, "content": st.session_state.dom_content}]
                                    s, a = st.session_state.vm.chat(q, data, st.session_state.chat_history[:-1])
                                if s:
                                    st.markdown(a)
                                    st.session_state.chat_history.append({"role": "assistant", "content": a})
        st.markdown("</div>", unsafe_allow_html=True)
                                
    elif page == "History":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.title("History")
        
        history = st.session_state.vm.get_history(st.session_state.user["id"])
        
        if not history:
            st.info("No history found.")
        else:
            for scrape in history:
                with st.container(border=True):
                    st.markdown(f"**{scrape['url']}**")
                    st.caption(f"Date: {scrape['scraped_at'][:10]}")
                    if st.checkbox("View Reports", key=f"hist_{scrape['id']}"):
                        results = st.session_state.vm.get_results(scrape["id"])
                        if not results:
                            st.info("No extracted reports found for this scrape.")
                        else:
                            for r in results:
                                st.markdown(f"""
                                <div class='custom-card' style='margin-bottom: 10px;'>
                                    <p style='margin-bottom: 5px;'><strong>Prompt:</strong> {r['prompt']}</p>
                                    <div style='border-top: 1px solid #ccc; padding-top: 10px;'>
                                        {r['extracted_text']}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Profile":
        st.markdown("<div class='main-content'>", unsafe_allow_html=True)
        st.title("Profile")
        
        stats = st.session_state.vm.get_stats(st.session_state.user["id"])
        
        c1, c2 = st.columns(2)
        with c1: st.metric("Scrapes", stats['total_scrapes'])
        with c2: st.metric("Extractions", stats['total_results'])
            
        st.markdown("<br>", unsafe_allow_html=True)
        prof_col1, prof_col2 = st.columns(2, gap="large")
        
        with prof_col1:
            with st.container(border=True):
                st.subheader("Details")
                name = st.text_input("Name", value=st.session_state.user.get("full_name", ""))
                bio = st.text_area("Bio", value=st.session_state.user.get("bio", ""), height=100)
                if st.button("Update"):
                    s, m = st.session_state.vm.update_profile(st.session_state.user["id"], name, bio)
                    if s: st.toast("Updated!")
                    
        with prof_col2:
            with st.container(border=True):
                st.subheader("Security")
                op = st.text_input("Old Password", type="password")
                np = st.text_input("New Password", type="password")
                if st.button("Change"):
                    s, m = st.session_state.vm.change_password(st.session_state.user["id"], op, np, np)
                    if s: st.success(m)
                    else: st.error(m)
        st.markdown("</div>", unsafe_allow_html=True)
