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
import time



def process_chat(
    db: Session,
    user_id: int,
    conversation_id: int,
    user_message: str,
):
    request_start = time.perf_counter()

    conversation = get_conversation(
        db,
        conversation_id,
    )

    if (
        conversation is None
        or conversation.user_id != user_id
    ):
        raise ValueError("Conversation not found")

    save_message(
        db,
        conversation_id,
        "user",
        user_message,
    )

    history = get_conversation_messages(
        db,
        conversation_id,
    )

    if len(history) == 1:
        title = generate_title(user_message)

        update_conversation_title(
            db,
            conversation,
            title,
        )

    prompt = build_prompt(
        history,
        user_message,
    )

    gemini_start = time.perf_counter()

    ai_response = chat(prompt)

    print(
        f"Gemini took {time.perf_counter() - gemini_start:.2f}s"
    )

    save_message(
        db,
        conversation_id,
        "assistant",
        ai_response,
    )

    print(
        f"Total request took {time.perf_counter() - request_start:.2f}s"
    )

    return ai_response