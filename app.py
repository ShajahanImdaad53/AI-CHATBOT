import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import base64

# SET PAGE CONFIG FIRST!
st.set_page_config(page_title="AI Chatbot", page_icon="🚀", layout="centered")

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_base64 = get_base64_of_bin_file("assets/liquid_bg.png")

# ==============================
# CSS FOR LIQUID GLASS AESTHETICS 
# ==============================
st.markdown(f"""
<style>
    /* Import new fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif !important;
    }}

    /* Use the generated Liquid Background Image */
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Beautiful Title Gradient */
    h1 {{
        background: -webkit-linear-gradient(45deg, #00FF7F, #00BFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800;
        text-align: center;
        margin-bottom: 25px;
        padding-top: 10px;
        text-shadow: 0px 4px 15px rgba(0, 255, 127, 0.3);
    }}

    /* LIQUID GLASS Chat Messages */
    [data-testid="stChatMessage"] {{
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 12px;
        /* The liquid glass effect */
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) saturate(120%);
        -webkit-backdrop-filter: blur(20px) saturate(120%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }}
    
    /* User Message slight tint */
    [data-testid="stChatMessage"]:nth-child(even) {{
        border: 1px solid rgba(0, 255, 127, 0.2);
    }}

    /* Assistant Message slight tint */
    [data-testid="stChatMessage"]:nth-child(odd) {{
        border: 1px solid rgba(0, 191, 255, 0.2);
    }}

    /* Chat input liquid styling */
    .stChatInputContainer {{
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        background: rgba(10, 14, 23, 0.6) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }}
    .stChatInputContainer:focus-within {{
        border: 1px solid #00FF7F !important;
        box-shadow: 0 4px 20px rgba(0, 255, 127, 0.3);
    }}

    /* Custom colored avatars */
    .stChatMessageAvatarUser {{
        background-color: #00FF7F !important;
    }}
    .stChatMessageAvatarAssistant {{
        background-color: #00BFFF !important;
    }}
</style>
""", unsafe_allow_html=True)

# Load Env Vars
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("Error initializing Groq client. Check your API key.")
    client = None

st.title("🌟 AI Chatbot with Imdaad")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show entire chat history
for message in st.session_state.messages:
    # Use standard Streamlit chat components
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new prompt
prompt = st.chat_input("Ask me anything...")

if prompt and client:
    # Append the user message and print to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Show a cool spinner while thinking...
        with st.spinner("✨ AI is thinking..."):
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            reply = res.choices[0].message.content
        
        # Add assistant reply to message history and display it
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        # In case the free tier API is exhausted or offline
        error_msg = f"**Error occurred:** {str(e)}"
        st.error(error_msg)