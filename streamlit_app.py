import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import base64
from datetime import datetime

# SET PAGE CONFIG FIRST!
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_base64 = get_base64_of_bin_file("assets/liquid_bg.png")

# ==============================
# CUSTOM HTML BUBBLE ARCHITECTURE
# ==============================
custom_css = f"""
<style>
    /* Import new fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif !important;
    }}

    /* Deep Space Background */
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp > header {{
        background-color: transparent;
    }}

    /* Main Container overrides */
    .main {{
        padding-top: 1rem !important;
        display: flex;
        justify-content: center;
    }}
    .block-container {{
        max-width: 900px !important;
    }}

    /* THE GLASS CHAT WINDOW */
    .glass-chat-window {{
        background: rgba(20, 25, 45, 0.4);
        backdrop-filter: blur(25px) saturate(120%);
        -webkit-backdrop-filter: blur(25px) saturate(120%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        margin-bottom: 90px;
        height: 75vh;
    }}

    /* HEADER */
    .chat-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 30px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(0, 0, 0, 0.2);
    }}
    .chat-header h2 {{
        margin: 0;
        font-size: 1.6rem;
        font-weight: 500;
        color: #ffffff;
        text-shadow: 0px 2px 10px rgba(255,255,255,0.1);
    }}
    .header-right {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    .status-dot {{
        height: 10px;
        width: 10px;
        background-color: #00FF7F;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00FF7F;
    }}
    .status-text {{
        color: #00FF7F;
        font-weight: 400;
        font-size: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* MESSAGES AREA */
    .messages-container {{
        padding: 30px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 25px;
        height: 100%;
        overflow-x: hidden;
    }}

    /* BUBBLE WRAPPERS */
    .msg-wrapper {{
        display: flex;
        flex-direction: column;
        max-width: 80%;
    }}
    .msg-wrapper.right {{
        align-self: flex-end;
    }}
    .msg-wrapper.left {{
        align-self: flex-start;
    }}

    /* BUBBLE STYLES */
    .chat-bubble {{
        padding: 16px 20px;
        border-radius: 15px;
        font-size: 15.5px;
        line-height: 1.5;
        color: #E2E8F0;
        background: rgba(25, 35, 55, 0.5);
        backdrop-filter: blur(10px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
    }}
    .chat-bubble.user {{
        border: 1px solid rgba(0, 191, 255, 0.3);
        box-shadow: 0 0 15px rgba(0, 191, 255, 0.05);
    }}
    .chat-bubble.bot {{
        border: 1px solid rgba(0, 255, 127, 0.3);
        box-shadow: 0 0 15px rgba(0, 255, 127, 0.05);
    }}

    /* LABELS */
    .user-label {{
        color: #00BFFF;
        font-weight: 600;
        margin-right: 8px;
    }}
    .bot-label {{
        color: #00FF7F;
        font-weight: 600;
        margin-right: 8px;
    }}

    /* TIMESTAMP */
    .timestamp {{
        font-size: 12px;
        color: rgba(255, 255, 255, 0.3);
        margin-top: 8px;
        text-align: right;
        padding-right: 5px;
    }}

    /* SCROLLBAR */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }}

    /* GLOWING INPUT BAR */
    .stChatInputContainer {{
        border-radius: 30px !important;
        border: 2px solid rgba(0, 255, 127, 0.5) !important;
        background: rgba(10, 15, 30, 0.8) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        box-shadow: 0 0 25px rgba(0, 255, 127, 0.15), inset 0 0 10px rgba(0, 255, 127, 0.05);
        padding-left: 10px;
        padding-right: 5px;
        margin-bottom: 20px;
    }}
    .stChatInputContainer:focus-within {{
        border: 2px solid #00BFFF !important;
        box-shadow: 0 0 30px rgba(0, 191, 255, 0.25), inset 0 0 15px rgba(0, 191, 255, 0.1);
    }}
    
    /* Make standard Streamlit Markdown completely invisible to prevent ghosting */
    div[data-testid="stChatMessage"] {{ display: none !important; }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Application Logic
load_dotenv(override=True)

# First try to get the API key from Streamlit secrets, then fallback to environment variables (.env)
try:
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

try:
    if not api_key:
        raise ValueError("API Key is missing. Please set GROQ_API_KEY in .env or Streamlit secrets.")
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing Groq client: {str(e)}")
    client = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Generate custom HTML for the overarching chat window
html_content = """<div class="glass-chat-window">
<div class="chat-header">
<h2>AI Assistant</h2>
<div class="header-right">
<div class="status-text"><span class="status-dot"></span> Online</div>
</div>
</div>
<div class="messages-container" id="chatbox">
"""

def generate_message_html(role, content, time_str):
    if role == "user":
        return f"""<div class="msg-wrapper right">
<div class="chat-bubble user">
<span class="user-label">User:</span>{content}
</div>
<div class="timestamp">{time_str}</div>
</div>"""
    else:
        return f"""<div class="msg-wrapper left">
<div class="chat-bubble bot">
<span class="bot-label">AI Chatbot:</span>{content}
</div>
<div class="timestamp">{time_str}</div>
</div>"""

# Render history explicitly
for ms in st.session_state.messages:
    time_str = ms.get("time", datetime.now().strftime("%I:%M %p"))
    html_content += generate_message_html(ms["role"], ms["content"], time_str)

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
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    try:
        with st.spinner("AI is typing..."):
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            reply = res.choices[0].message.content
        
        current_time = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({"role": "assistant", "content": reply, "time": current_time})
        st.rerun()

    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        st.error(error_msg)