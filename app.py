import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# SET PAGE CONFIG FIRST!
st.set_page_config(page_title="AI Chatbot", page_icon="🚀", layout="centered")

# ==============================
# CSS FOR PREMIUM AESTHETICS 
# ==============================
st.markdown("""
<style>
    /* Gradient Background Effect */
    .stApp {
        background: radial-gradient(circle at top right, rgb(20, 30, 48) 0%, rgb(10, 14, 23) 100%);
    }

    /* Beautiful Title Gradient */
    h1 {
        background: -webkit-linear-gradient(45deg, #00FF7F, #00BFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        text-align: center;
        margin-bottom: 25px;
        padding-top: 10px;
    }

    /* Custom Glassmorphism styling for chat messages container */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 12px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    /* User Message distinct style */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(0, 255, 127, 0.08);
        border: 1px solid rgba(0, 255, 127, 0.2);
    }

    /* Assistant Message distinct style */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(0, 191, 255, 0.08);
        border: 1px solid rgba(0, 191, 255, 0.2);
    }

    /* Chat input styling */
    .stChatInputContainer {
        border-radius: 24px !important;
        border: 1px solid rgba(0, 255, 127, 0.5) !important;
        background-color: rgba(20, 27, 41, 0.9) !important;
        box-shadow: 0 4px 15px rgba(0, 255, 127, 0.1);
    }
    .stChatInputContainer:focus-within {
        border: 1px solid #00FF7F !important;
        box-shadow: 0 4px 20px rgba(0, 255, 127, 0.3);
    }

    /* Custom colored avatars via text styling if you want text fallbacks to match */
    .stChatMessageAvatarUser {
        background-color: #00FF7F;
    }
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