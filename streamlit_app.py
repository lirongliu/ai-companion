import openai
import streamlit as st
import os

# Use environment variable or hardcoded key (for local testing only)
# openai.api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"
openai.api_key = "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"

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
        st.experimental_rerun()
