from app.models.message import Message


SYSTEM_PROMPT = """
You are Titan.

Titan is an intelligent AI assistant that provides accurate,
clear and practical answers.

Answer in Markdown.

Be concise unless the user asks for details.
"""


def build_prompt(messages: list[Message], user_message: str):

    prompt = SYSTEM_PROMPT.strip()

    prompt += "\n\nConversation History:\n"

    for message in messages:

        prompt += f"\n{message.role}: {message.content}"

    prompt += f"\n\nuser: {user_message}"

    return prompt