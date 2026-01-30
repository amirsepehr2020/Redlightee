from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def ask_ai(user_message):
    try:
        completion = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return completion.choices[0].message.content

    except Exception as e:
        return "یه مشکلی پیش اومد 🤕"
