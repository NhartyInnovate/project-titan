from app.services.gemini import generate_response


def chat(prompt: str):
    return generate_response(prompt)