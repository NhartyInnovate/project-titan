from sqlalchemy.orm import Session

from app.crud.conversation import (
    get_conversation,
    update_conversation_title,
)

from app.crud.message import (
    save_message,
    get_conversation_messages,
)

from app.services.ai import chat
from app.services.prompt_builder import build_prompt
from app.services.title_generator import generate_title


def process_chat(
    db: Session,
    conversation_id: int,
    user_message: str,
):

    conversation = get_conversation(
        db,
        conversation_id,
    )

    if conversation is None:
        raise ValueError("Conversation not found")

    # Save the user's message
    save_message(
        db,
        conversation_id,
        "user",
        user_message,
    )

    # Load conversation history
    history = get_conversation_messages(
        db,
        conversation_id,
    )

    # Generate a title ONLY if this is the first message
    if len(history) == 1:
        title = generate_title(user_message)

        update_conversation_title(
            db,
            conversation,
            title,
        )

    # Build the prompt for Gemini
    prompt = build_prompt(
        history,
        user_message,
    )

    # Get AI response
    ai_response = chat(prompt)

    # Save AI response
    save_message(
        db,
        conversation_id,
        "assistant",
        ai_response,
    )

    return ai_response