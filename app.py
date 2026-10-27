
import streamlit as st
from ollama import chat
from collections import Counter
import re


# Function to count repeated words
def count_repeated_words(text):
    words = re.findall(r"\b\w+\b", text.lower())
    word_counts = Counter(words)

    repeated_words = {
        word: count
        for word, count in word_counts.items()
        if count > 1
    }

    return repeated_words


# Page title
st.title("My LLM Chatbot")
st.write("Welcome to my local AI chatbot!")


# Create conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar for text analysis
with st.sidebar:
    st.header("Text Analysis")

    # Get user messages
    user_messages = [
        message["content"]
        for message in st.session_state.messages
        if message["role"] == "user"
    ]

    # Get AI messages
    ai_messages = [
        message["content"]
        for message in st.session_state.messages
        if message["role"] == "assistant"
    ]

    # User character count
    if user_messages:
        st.write("User character count:", len(user_messages[-1]))
    else:
        st.write("User character count: 0")

    # AI character count
    if ai_messages:
        st.write("AI character count:", len(ai_messages[-1]))
    else:
        st.write("AI character count: 0")

    # Token usage
    st.subheader("Token Usage")
    st.write(
        "Prompt tokens:",
        st.session_state.get("prompt_tokens", 0)
    )
    st.write(
        "Generated tokens:",
        st.session_state.get("generated_tokens", 0)
    )

    # User repeated words
    st.subheader("Repeated Words")

    if user_messages:
        user_repeated = count_repeated_words(user_messages[-1])
        st.write("User repeated words:", user_repeated)
    else:
        st.write("User repeated words: None")

    # AI repeated words
    if ai_messages:
        ai_repeated = count_repeated_words(ai_messages[-1])
        st.write("AI repeated words:", ai_repeated)
    else:
        st.write("AI repeated words: None")


# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Generate AI response
    with st.spinner("AI is thinking..."):
        response = chat(
            model="qwen2.5:3b",
            messages=st.session_state.messages
        )

    # Save token usage
    st.session_state.prompt_tokens = response.prompt_eval_count or 0
    st.session_state.generated_tokens = response.eval_count or 0

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.message.content
        }
    )

    # Refresh page
    st.rerun()
