import openai
import streamlit as st
import os

# Use environment variable or hardcoded key (for local testing only)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Companion", layout="centered")
st.title("🤖 Your AI Companion")

# Set up assistant using new API
client = openai.OpenAI(api_key=openai.api_key)

# System message
system_prompt = {
    "role": "system",
    "content": (
        "You are a warm, emotionally intelligent AI companion named Mira. "
        "You are here to listen empathetically, reflect feelings back to the user, "
        "and ask thoughtful follow-up questions. Don't mention you're an AI. "
        "Avoid giving generic advice. Use gentle, human-like tone."
    )
}

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# Show chat
for msg in st.session_state.messages[1:]:
    role = "🧑 You" if msg["role"] == "user" else "🤖 Mira"
    st.markdown(f"**{role}:** {msg['content']}")

# Input box
user_input = st.text_area("Your thoughts...", height=100)

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Mira is thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()


# Debug button to print all messages to the console
if st.button("🔍 Print Chat History to Console"):
    for msg in st.session_state.messages:
        print(f"{msg['role']}: {msg['content']}")