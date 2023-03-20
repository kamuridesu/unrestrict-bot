from .grabber import get_public_chat_id_from_name


async def get_message_informations(message: str) -> dict:
    if "https://t.me/" in message:
        message_data = message.split("/")
        message_id_in_group = int(message_data[-1].split("?")[0])
        # Private
        if "https://t.me/c/" in message:
            ...
        # public
        else:
            chat_name = message_data[3]
            chat_id = await get_public_chat_id_from_name(chat_name)
            return {
                "chat_name": chat_name,
                "chat_id": chat_id,
                "message_id": message_id_in_group,
            }
    return {}
