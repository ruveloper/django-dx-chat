from django.contrib.auth import get_user_model
from django.db.models import Model, ObjectDoesNotExist


def get_or_none(model: Model, *args, **kwargs) -> Model | None:
    """Get a unique object from DB if exists, otherwise return None"""
    try:
        return model.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        return None


def generate_chat_room_name(logged_user: str, chat_user: str):
    """
    Check for the existence of the chat_user and return a consistent chat room name made with both usernames.
    :Example:
    :param logged_user: authenticated user
    :param chat_user: user to open a chat
    :return: room_name: a consistence chat room name
    """
    user_model = get_user_model()
    chat_user_obj = get_or_none(user_model, username=chat_user)
    if not chat_user_obj:
        return None
    return "-".join(sorted([logged_user, chat_user]))
