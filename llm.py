from huggingface_hub import InferenceClient
client = InferenceClient(
    api_key="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"
)

MODEL = "meta-llama/Llama-3.1-8B-Instruct"

# Chat memory
chat_history = [
    {
        "role": "system",
            "content": """
You are Mawzoon, an intelligent personal financial advisor focused on budgeting, saving, and smart spending.

Rules:
- Give clear, practical financial advice.
- Keep responses short and easy to understand.
- Maximum 3 concise sentences.
- Be direct, realistic, and helpful.
- Suggest actionable steps when possible.
- Avoid long explanations or generic motivation.
- If the user asks about risky financial decisions, mention possible risks briefly.
- Use a friendly and confident tone.
"""
    }
]

def ask_llm(prompt):
    global chat_history

    # add user message
    chat_history.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat_completion(
        model=MODEL,
        messages=chat_history,
        max_tokens=120,
        temperature=0.5
    )

    reply = response.choices[0].message.content

    # save AI reply
    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    # keep last 10 messages only
    if len(chat_history) > 12:
        chat_history = [chat_history[0]] + chat_history[-10:]

    return reply