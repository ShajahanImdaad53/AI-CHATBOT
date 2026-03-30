from urllib import response

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("AI Chatbot with Imdaad")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.write(f"{message['role']}: {message['content']}")


prompt = st.chat_input("Ask me anything")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with  st.chat_message("user"):
        st.write(f"User: {prompt}")

    res= client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages,
    )

    reply = res.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.spinner("Generating response..."):
        st.write(f"Assistant: {reply}")

# Load environment variables from .env file