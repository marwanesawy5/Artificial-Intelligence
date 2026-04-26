from huggingface_hub import InferenceClient
client = InferenceClient(
    api_key="Your_Secret_API"
)

MODEL = "meta-llama/Llama-3.1-8B-Instruct"

# Chat memory
chat_history = [
    {
        "role": "system",
        "content": """
You are Mawzoon, a smart financial advisor.

Rules:
- Answer briefly.
- Maximum 3 short sentences.
- Be direct and practical.
- No unnecessary explanation.
- Remember previous conversation context.
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