from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

# Function to get response from Gemini
def get_gemini_response(question):
    return chat.send_message(question, stream=True)

# Page Configuration
st.set_page_config(page_title="💬 Gemini Chat", page_icon="✨", layout="centered")

# App Header
st.title("🤖 Gemini LLM Chatbot")
st.caption("Powered by Google's Gemini 1.5 Pro")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history in a conversational format
for role, text in st.session_state.chat_history:
    with st.chat_message("user" if role == "You" else "assistant"):
        st.markdown(text)

# Chat input at bottom
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append(("You", prompt))

    # Get and stream Gemini's response
    response_text = ""
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        for chunk in get_gemini_response(prompt):
            response_text += chunk.text
            response_placeholder.markdown(response_text + "▌")

    st.session_state.chat_history.append(("Bot", response_text))
