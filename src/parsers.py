"""Parses the messages to check for the following:
- Public chat messages
- Private chat messages
- Private chat links"""

from src.grabber import get_public_chat_id_from_name


async def get_private_group_link(message: str) -> None:
    chat_hash = ""
    if "https://t.me/+" in message:
        chat_hash = message.split("+")[-1]
    elif "https://t.me/joinchat/" in message:
        chat_hash = message.split("/")[-1]
    if chat_hash:
        return {"type": "invite", "hash": chat_hash}
    return {}


async def get_message_informations(message: str) -> dict:
    if link_details := await get_private_group_link(message):
        return link_details
    if "https://t.me/" in message:
        message_data = message.split("/")
        message_id_in_group = int(message_data[-1].split("?")[0])
        # Private
        if "https://t.me/c/" in message:
            return {
                "type": "message",
                "chat_id": int(f"-100{message_data[4]}"),
                "message_id": message_id_in_group,
            }
        # public
        else:
            chat_name = message_data[3]
            chat_id = await get_public_chat_id_from_name(chat_name)
            return {
                "type": "message",
                "chat_name": chat_name,
                "chat_id": chat_id,
                "message_id": message_id_in_group,
            }
    return {"type": "unknown"}
