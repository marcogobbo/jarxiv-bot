# pylint: disable=C0116,C0114

from telegram.ext import ContextTypes


async def send_message(chat_id: int, context: ContextTypes, text: str) -> None:
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
    )


async def item_message(
    chat_id: int, context: ContextTypes, item: str, keys: str, action: str
) -> None:
    messages = {
        "append": f"<b>{item}</b> has been added to the {keys} list!",
        "remove": f"<b>{item}</b> has been removed from the {keys} list!",
        "duplicate": f"<b>{item}</b> is already in the {keys} list!",
        "missing": f"<b>{item}</b> is not in the {keys} list!",
    }
    await send_message(
        chat_id,
        context,
        messages[action],
    )


async def config_file_status(chat, context, status):
    if status == "created":
        message = f"Configuration file created for the {chat['type']} chat <b>{chat['name']}</b> with ID <b>{chat['id']}</b>."
    elif status == "exists":
        message = f"Configuration file for the {chat['type']} chat <b>{chat['name']}</b> with ID <b>{chat['id']}</b> already exists."
    elif status == "missing":
        message = f"Configuration file not found for the {chat['type']} chat <b>{chat['name']}</b> with ID <b>{chat['id']}</b>.\nPlease initialize the configuration with <b>/start</b."
    else:
        message = f"There is an issue with the configuration for the {chat['type']} chat <b>{chat['name']}</b> with ID <b>{chat['id']}</b>."
    await send_message(chat["id"], context, message)
