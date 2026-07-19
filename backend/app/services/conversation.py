from app.crud.conversation import (
    create_conversation,
    get_user_conversations,
    get_conversation,
    delete_conversation,
    update_conversation_title,
)


def rename_conversation(
    db,
    conversation,
    title: str,
):
    return update_conversation_title(
        db=db,
        conversation=conversation,
        title=title,
    )