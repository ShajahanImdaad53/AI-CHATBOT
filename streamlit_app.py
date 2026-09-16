import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import base64
from datetime import datetime
import pypdf
from urllib.parse import quote

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

# ==============================
# CUSTOM HTML BUBBLE ARCHITECTURE
# ==============================
custom_css = f"""
<style>
    /* Import new fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif !important;
        background-color: #000000 !important;
    }}

    /* Solid Black with top-left purple glow */
    .stApp {{
        background: radial-gradient(circle at 0% 0%, #3a005c 0%, #000000 40%);
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
    
    /* Responsive Desktop/Mobile Views */
    @media (min-width: 768px) {{
        .block-container {{
            max-width: 900px !important; /* Desktop width */
        }}
        .glass-chat-window {{
            border-radius: 20px;
            height: 80vh;
        }}
    }}
    @media (max-width: 767px) {{
        .block-container {{
            max-width: 100% !important; /* Mobile width */
            padding-left: 0px !important;
            padding-right: 0px !important;
        }}
        .glass-chat-window {{
            border-radius: 0px; /* Flush to edges on mobile */
            height: 85vh;
            border-left: none;
            border-right: none;
        }}
    }}

    /* THE GLASS CHAT WINDOW */
    .glass-chat-window {{
        background: transparent;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        margin-bottom: 90px;
        height: 80vh;
    }}

    /* HEADER - exact match */
    .chat-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        background: transparent;
    }}
    .header-left {{
        display: flex;
        align-items: center;
        gap: 15px;
        color: white;
        font-size: 20px;
        cursor: pointer;
    }}
    .header-center {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .header-center h2 {{
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
    }}
    .header-center span {{
        font-size: 0.8rem;
        color: #A3A3A3;
    }}
    .header-right {{
        color: white;
        font-size: 20px;
        cursor: pointer;
    }}

    /* MESSAGES AREA */
    .messages-container {{
        padding: 20px 10px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
        height: 100%;
        overflow-x: hidden;
    }}

    /* BUBBLE WRAPPERS */
    .msg-wrapper {{
        display: flex;
        flex-direction: row;
        align-items: flex-end;
        gap: 8px;
        max-width: 90%;
    }}
    .msg-wrapper.right {{
        align-self: flex-end;
        flex-direction: row-reverse;
    }}
    .msg-wrapper.left {{
        align-self: flex-start;
    }}

    /* BUBBLE STYLES */
    .chat-bubble {{
        padding: 15px;
        font-size: 15px;
        line-height: 1.4;
        color: #E2E8F0;
        position: relative;
    }}
    .chat-bubble.user {{
        background: linear-gradient(135deg, #d946ef, #8b5cf6);
        border-radius: 20px 20px 5px 20px; /* Sharp bottom-right */
        box-shadow: 0 4px 15px rgba(217, 70, 239, 0.2);
    }}
    .chat-bubble.bot {{
        background: #1C1C1E;
        border-radius: 20px 20px 20px 5px; /* Sharp bottom-left */
        border: 1px solid rgba(255,255,255,0.05);
        color: #D4D4D4;
    }}

    /* BOT ACTION ROW */
    .bot-actions {{
        display: flex;
        gap: 15px;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.05);
        color: #888;
        font-size: 16px;
    }}
    .bot-actions span {{
        cursor: pointer;
    }}
    .bot-actions span:hover {{
        color: #fff;
    }}

    /* AVATARS */
    .avatar {{
        width: 25px;
        height: 25px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }}
    .avatar.user-avatar {{
        background: #444;
        background-image: url('https://api.dicebear.com/7.x/avataaars/svg?seed=Imdu');
        background-size: cover;
    }}
    .avatar.bot-avatar {{
        background: transparent;
        border: 1px solid #d946ef;
        color: #d946ef;
    }}

    /* SCROLLBAR */
    ::-webkit-scrollbar {{
        width: 5px;
    }}
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }}

    /* PILL INPUT BAR */
    .stChatInputContainer {{
        border-radius: 40px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(10, 10, 15, 0.9) !important;
        padding-left: 15px;
        padding-right: 15px;
        margin-bottom: 20px;
    }}
    .stChatInputContainer:focus-within {{
        border: 1px solid #d946ef !important;
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

st.sidebar.title("✨ Imdu AI Features")
feature = st.sidebar.radio("Navigate", ["Chat", "PDF Q&A", "Image Generation"])

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
    st.markdown("Generate images instantly using Pollinations AI.")
    img_prompt = st.text_input("Enter your image prompt:", placeholder="E.g., A futuristic cyberpunk city at sunset")
    if img_prompt:
        encoded_prompt = quote(img_prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        with st.spinner("Generating image..."):
            st.image(image_url, caption=img_prompt, use_container_width=True)

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
                    )
                )
                reply = response.text
            
            current_time = datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({"role": "assistant", "content": reply, "time": current_time})
            st.rerun()

        except Exception as e:
            error_msg = f"Error occurred: {str(e)}"
            st.error(error_msg)