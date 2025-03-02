import openai

API_KEY = "YOUR_OPENAI_API_KEY"

def generate_response(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]

response_text = generate_response("Hello, how are you?")
print("AI Response:", response_text)
