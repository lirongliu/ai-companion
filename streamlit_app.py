import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = "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"

st.set_page_config(page_title="AI Companion", layout="centered")
st.title("🤖 Your AI Companion")

# System prompt to shape the companion's personality
system_prompt = {
    "role": "system",
    "content": (
        "You are a warm, emotionally intelligent AI companion named Mira. "
        "You are here to listen empathetically, reflect feelings back to the user, "
        "and ask thoughtful follow-up questions. Don't mention you're an AI. "
        "Avoid giving generic advice. Use gentle, human-like tone."
    )
}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# Display conversation history
for msg in st.session_state.messages[1:]:
    role = "🧑 You" if msg["role"] == "user" else "🤖 Mira"
    st.markdown(f"**{role}:** {msg['content']}")

# User input
user_input = st.text_area("Your thoughts...", height=100)
if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Mira is thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.experimental_rerun()
