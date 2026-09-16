import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import base64
from datetime import datetime
import pypdf
from urllib.parse import quote
from streamlit_option_menu import option_menu

# SET PAGE CONFIG FIRST!
st.set_page_config(page_title="Imdu AI", page_icon="🤖", layout="wide")

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_base64 = get_base64_of_bin_file("assets/liquid_bg.png")

with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 32px; font-weight: 800; background: -webkit-linear-gradient(#d946ef, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>✨ Imdu AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 14px; margin-bottom: 20px;'>Your Multimodal Assistant</p>", unsafe_allow_html=True)
    is_dark_mode = st.toggle("🌙 Dark Mode", value=True)

theme_vars = """
:root {
    --bg-sidebar: #09090b;
    --bg-mobile: #000000;
    --bg-mobile-gradient: radial-gradient(circle at 0% 0%, #3a005c 0%, #000000 40%);
    --bg-desktop: #131314;
    --text-main: #ffffff;
    --text-bot: #D4D4D4;
    --text-bot-desktop: #e3e3e3;
    --border-subtle: rgba(255,255,255,0.05);
    --border-input: rgba(255,255,255,0.2);
    --bg-input-mobile: rgba(10, 10, 15, 0.9);
    --bg-input-desktop: #1e1f20;
    --bg-bot-mobile: #1C1C1E;
    --bg-user-desktop: #282a2c;
    --radio-bg: rgba(255, 255, 255, 0.05);
    --radio-border: rgba(255, 255, 255, 0.1);
    --text-user-desktop: #e3e3e3;
}
""" if is_dark_mode else """
:root {
    --bg-sidebar: #f9fafb;
    --bg-mobile: #ffffff;
    --bg-mobile-gradient: radial-gradient(circle at 0% 0%, #f3e8ff 0%, #ffffff 40%);
    --bg-desktop: #ffffff;
    --text-main: #111827;
    --text-bot: #374151;
    --text-bot-desktop: #111827;
    --border-subtle: rgba(0,0,0,0.1);
    --border-input: rgba(0,0,0,0.2);
    --bg-input-mobile: rgba(255, 255, 255, 0.9);
    --bg-input-desktop: #f3f4f6;
    --bg-bot-mobile: #f3f4f6;
    --bg-user-desktop: #e5e7eb;
    --radio-bg: rgba(0, 0, 0, 0.05);
    --radio-border: rgba(0, 0, 0, 0.1);
    --text-user-desktop: #111827;
}
"""

# ==============================
# CUSTOM HTML BUBBLE ARCHITECTURE
# ==============================
custom_css = f"""
<style>
    {theme_vars}
    
    /* Import new fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;800&display=swap');
    
    /* Make standard Streamlit Markdown completely invisible to prevent ghosting */
    div[data-testid="stChatMessage"] {{ display: none !important; }}

    /* =========================================
       SIDEBAR NAVIGATION STYLING
       ========================================= */
    [data-testid="stSidebar"] {{
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }}
    [data-testid="stSidebar"] label[data-baseweb="radio"] {{
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 16px 20px !important;
        background: var(--radio-bg) !important;
        border: 1px solid var(--radio-border) !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        color: var(--text-main) !important;
    }}
    [data-testid="stSidebar"] label[data-baseweb="radio"]:hover {{
        background: rgba(217, 70, 239, 0.2) !important;
        border-color: rgba(217, 70, 239, 0.5) !important;
        transform: translateY(-2px) !important;
    }}
    /* Hide default radio circle */
    [data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {{
        display: none !important; 
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 0px !important;
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
    }}

    /* =========================================
       MOBILE VIEW (NEON APP CLONE)
       ========================================= */
    @media (max-width: 767px) {{
        html, body, [class*="css"] {{
            font-family: 'Outfit', sans-serif !important;
            background-color: var(--bg-mobile) !important;
        }}

        .stApp {{
            background: var(--bg-mobile-gradient);
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .stApp > header {{ background-color: transparent; }}

        .main {{ padding-top: 0 !important; }}
        .block-container {{
            max-width: 100% !important;
            padding: 0 !important;
        }}

        .glass-chat-window {{
            background: transparent;
            display: flex;
            flex-direction: column;
            margin-bottom: 90px;
            height: 85vh;
        }}

        .chat-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-subtle);
            background: transparent;
        }}
        .header-left, .header-right {{ color: var(--text-main); font-size: 20px; }}
        .header-center {{ display: flex; flex-direction: column; align-items: center; }}
        .header-center h2 {{ margin: 0; font-size: 1.1rem; font-weight: 600; color: var(--text-main); }}
        .header-center span {{ font-size: 0.8rem; color: #A3A3A3; }}

        .messages-container {{
            padding: 20px 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            height: 100%;
        }}

        .msg-wrapper {{
            display: flex;
            flex-direction: row;
            align-items: flex-end;
            gap: 8px;
            max-width: 95%;
        }}
        .msg-wrapper.right {{ align-self: flex-end; flex-direction: row-reverse; }}
        .msg-wrapper.left {{ align-self: flex-start; }}

        .chat-bubble {{
            padding: 15px;
            font-size: 18px; /* Increased font size */
            line-height: 1.4;
            position: relative;
        }}
        .chat-bubble.user {{
            background: linear-gradient(135deg, #d946ef, #8b5cf6);
            border-radius: 20px 20px 5px 20px; 
            color: #ffffff;
        }}
        .chat-bubble.bot {{
            background: var(--bg-bot-mobile);
            border-radius: 20px 20px 20px 5px; 
            border: 1px solid var(--border-subtle);
            color: var(--text-bot);
        }}

        .bot-actions {{
            display: flex;
            gap: 15px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid var(--border-subtle);
            color: #888;
            font-size: 16px;
        }}

        .avatar {{
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .avatar.user-avatar {{ background: #444; background-image: url('https://api.dicebear.com/7.x/avataaars/svg?seed=Imdu'); background-size: cover; }}
        .avatar.bot-avatar {{ border: 1px solid #d946ef; color: #d946ef; font-size: 14px;}}

        .stChatInputContainer {{
            border-radius: 40px !important;
            border: 1px solid var(--border-input) !important;
            background: var(--bg-input-mobile) !important;
            padding: 0 15px;
            margin: 0 10px 20px 10px;
        }}
        .stChatInputContainer:focus-within {{ border: 1px solid #d946ef !important; }}
    }}

    /* =========================================
       DESKTOP VIEW (GEMINI CLONE)
       ========================================= */
    @media (min-width: 768px) {{
        html, body, [class*="css"] {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            background-color: var(--bg-desktop) !important;
        }}
        
        .stApp {{ background: var(--bg-desktop) !important; }}
        .stApp > header {{ background-color: transparent; }}

        .main {{ padding-top: 2rem !important; display: flex; justify-content: center; }}
        .block-container {{ max-width: 900px !important; }}

        .glass-chat-window {{
            background: transparent;
            display: flex;
            flex-direction: column;
            margin-bottom: 90px;
            height: 80vh;
        }}
        
        .chat-header {{ display: none !important; }}

        .messages-container {{
            padding: 20px 40px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 24px;
            height: 100%;
        }}

        .msg-wrapper {{
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            gap: 16px;
            max-width: 85%;
        }}
        .msg-wrapper.right {{ align-self: flex-end; flex-direction: row-reverse; }}
        .msg-wrapper.left {{ align-self: flex-start; }}

        .chat-bubble {{
            font-size: 18px; /* Increased font size */
            line-height: 1.6;
            color: var(--text-bot-desktop);
        }}
        .chat-bubble.user {{
            background: var(--bg-user-desktop);
            color: var(--text-user-desktop);
            border-radius: 24px;
            padding: 12px 24px;
        }}
        .chat-bubble.bot {{
            background: transparent;
            padding: 0;
            padding-top: 5px;
        }}

        .bot-actions {{ display: none !important; }}

        .avatar {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .avatar.user-avatar {{ display: none; }}
        .avatar.bot-avatar {{ 
            background: var(--bg-input-desktop); 
            color: #a8c7fa; 
            font-size: 20px;
        }}

        .stChatInputContainer {{
            background: var(--bg-input-desktop) !important;
            border: 1px solid var(--border-input) !important;
            border-radius: 30px !important;
            box-shadow: none !important;
            padding: 0 15px;
        }}
        
        /* Fix standard text colors in desktop view for markdown blocks */
        .chat-bubble.bot p, .chat-bubble.bot h1, .chat-bubble.bot h2, .chat-bubble.bot h3, .chat-bubble.bot li {{
            color: var(--text-bot-desktop) !important;
        }}
        
        /* Fix text color for input container placeholder */
        .stChatInputContainer textarea {{
            color: var(--text-bot-desktop) !important;
        }}
    }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# Application Logic
load_dotenv(override=True)

# First try to get the API key from Streamlit secrets, then fallback to environment variables (.env)
try:
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

try:
    if not api_key:
        raise ValueError("API Key is missing. Please set GEMINI_API_KEY in .env or Streamlit secrets.")
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing Gemini client: {str(e)}")
    client = None

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""

with st.sidebar:
    # Sidebar header is now handled above where we initialized the toggle
    
    feature = option_menu(
        menu_title=None,
        options=["Chat", "PDF Q&A", "Image Generation"],
        icons=["chat-dots-fill", "file-earmark-pdf-fill", "image-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#d946ef", "font-size": "20px"},
            "nav-link": {
                "font-size": "18px", 
                "font-weight": "bold", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "rgba(217, 70, 239, 0.1)"
            },
            "nav-link-selected": {"background-color": "rgba(217, 70, 239, 0.2)", "color": "#d946ef"},
        }
    )

if feature == "PDF Q&A":
    st.sidebar.markdown("---")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF document", type=["pdf"])
    if uploaded_file is not None:
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            st.session_state.pdf_context = text
            st.sidebar.success("PDF processed successfully! You can now ask questions about it in the chat.")
        except Exception as e:
            st.sidebar.error(f"Error processing PDF: {e}")

if feature == "Image Generation":
    st.markdown("## 🎨 AI Image Generation")
    st.markdown("Generate sharp, high-quality images instantly.")
    
    style_col, prompt_col = st.columns([1, 3])
    with style_col:
        img_style = st.selectbox("Choose a Style:", [
            "Realistic (High Quality)", 
            "Pencil Sketch", 
            "Pen Drawing", 
            "Watercolor"
        ])
    with prompt_col:
        img_prompt = st.text_input("Enter your image prompt:", placeholder="E.g., A futuristic cyberpunk city")
        
    if img_prompt:
        style_modifiers = ""
        if img_style == "Realistic (High Quality)":
            style_modifiers = ", highly detailed, sharp focus, 8k resolution, photorealistic, masterpiece"
        elif img_style == "Pencil Sketch":
            style_modifiers = ", detailed pencil sketch, graphite, shading, fine lines, sharp"
        elif img_style == "Pen Drawing":
            style_modifiers = ", detailed pen and ink drawing, crosshatching, sharp ink lines, masterpiece"
        elif img_style == "Watercolor":
            style_modifiers = ", beautiful watercolor painting, vibrant colors, artistic, sharp brush strokes"
            
        final_prompt = f"{img_prompt}{style_modifiers}"
        encoded_prompt = quote(final_prompt)
        
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true"
        
        with st.spinner(f"Generating {img_style.lower()}..."):
            st.image(image_url, caption=f"{img_prompt} ({img_style})", use_container_width=True)

elif feature in ["Chat", "PDF Q&A"]:
    # Generate custom HTML for the overarching chat window
    html_content = """<div class="glass-chat-window">
<div class="chat-header">
<div class="header-left">❮</div>
<div class="header-center">
<h2>Text writer</h2>
<span>Imdu AI</span>
</div>
<div class="header-right">⋮</div>
</div>
<div class="messages-container" id="chatbox">
"""

    def generate_message_html(role, content):
        if role == "user":
            return f"""<div class="msg-wrapper right">
<div class="avatar user-avatar"></div>
<div class="chat-bubble user">
{content}
</div>
</div>"""
        else:
            return f"""<div class="msg-wrapper left">
<div class="avatar bot-avatar">✨</div>
<div class="chat-bubble bot">
{content}
<div class="bot-actions">
<span>⧉</span>
<span>👍</span>
<span>👎</span>
<span>🔊</span>
<span style="margin-left: auto;">↻</span>
</div>
</div>
</div>"""

    # Render history explicitly
    for ms in st.session_state.messages:
        html_content += generate_message_html(ms["role"], ms["content"])

    html_content += """</div>
</div>"""

    # Render the single massive HTML layout
    st.markdown(html_content, unsafe_allow_html=True)

    # Process User Input
    prompt = st.chat_input("Type your message here...")

    if prompt and client:
        current_time = datetime.now().strftime("%I:%M %p")
        # Quick UX Trick: Add message and immediately rerun script to force HTML redrawing
        st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
        st.rerun()

    # Generation Step
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and client:
        try:
            with st.spinner("Imdu AI is typing..."):
                system_instruction = "Your name is Imdu AI. You were created by Imdaad Shajahan. Do not mention Meta or any other creator. Be helpful and intelligent."
                
                if st.session_state.pdf_context:
                    system_instruction += f"\n\nHere is context from an uploaded document that the user might refer to:\n{st.session_state.pdf_context}"

                contents = []
                for m in st.session_state.messages:
                    role = "user" if m["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": m["content"]}]})

                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        safety_settings=[
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                            ),
                            types.SafetySetting(
                                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                            ),
                        ]
                    )
                )
                reply = response.text
            
            current_time = datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({"role": "assistant", "content": reply, "time": current_time})
            st.rerun()

        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
            st.error(error_msg)