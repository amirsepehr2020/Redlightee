import os
import io
import base64
from huggingface_hub import InferenceClient

client = InferenceClient(
    api_key=os.environ.get("HF_TOKEN")
)

MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

def generate_image(prompt: str):
    try:
        image = client.text_to_image(
            prompt,
            model=MODEL
        )

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return f"data:image/png;base64,{img_base64}"

    except Exception as e:
        print("❌ IMAGE GEN ERROR:", e)
        return None
