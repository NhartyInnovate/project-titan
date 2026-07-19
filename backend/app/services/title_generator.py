from app.services.gemini import generate_response


def generate_title(first_message: str) -> str:
    prompt = f"""
Generate a very short conversation title.

Rules:
- Maximum 5 words.
- No quotation marks.
- No punctuation.
- Return ONLY the title.

User Message:
{first_message}
"""

    title = generate_response(prompt)

    return title.strip()