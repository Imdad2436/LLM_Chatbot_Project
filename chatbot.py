
from ollama import chat

from collections import Counter

import re

def count_repeated_words(text):
    words = re.findall(r"\b\w+\b", text.lower())
    word_counts = Counter(words)

    repeated_words = {
        word: count
        for word, count in word_counts.items()
        if count > 1
    }

    return repeated_words

messages = []

while True:
    user_question = input("You: ")

    if user_question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    messages.append({"role": "user", "content": user_question})

    response = chat(
        model="qwen2.5:3b",
        messages=messages
    )

    print("Chatbot:", response.message.content)

    ai_repeated_words = count_repeated_words(response.message.content)

    print("AI repeated words:", ai_repeated_words)

    print("Prompt tokens:", response.prompt_eval_count)

    print("Generated tokens:", response.eval_count)

    ai_characters = len(response.message.content)

    print("AI character count:", ai_characters)

    messages.append({"role": "assistant", "content": response.message.content})

    user_repeated_words = count_repeated_words(user_question)

    print("User repeated words:", user_repeated_words)

    user_characters = len(user_question)

    print("User character count:", user_characters)