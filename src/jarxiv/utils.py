# pylint: disable=C0116,C0114

from telegram import constants
from telegram.ext import ContextTypes


async def message(chat_id: int, context: ContextTypes, text: str) -> None:
    await context.bot.send_message(
        chat_id,
        text=text,
        parse_mode=constants.ParseMode.HTML,
    )


async def no_config_message(chat: dict, context: ContextTypes) -> None:
    await message(
        chat["id"],
        context,
        f"Configuration file not found for the {chat['type']} chat <b>{chat['name']}</b> with ID <b>{chat['id']}</b>.\nPlease initialize the configuration with <b>/start</b>",
    )


async def no_item_message(chat_id: id, context: ContextTypes, item: dict) -> None:
    item_name = list(item.keys())[0]
    await message(
        chat_id,
        context,
        f"You should specify the name of the {item_name} that you want add to the {item_name}s list!",
    )


async def add_item_message(
    chat_id: id, context: ContextTypes, item: str, keys: str
) -> None:
    await message(
        chat_id,
        context,
        f"{item} added to the {keys} list!",
    )


async def del_item_message(
    chat_id: id, context: ContextTypes, item: str, keys: str
) -> None:
    await message(
        chat_id,
        context,
        f"{item} removed to the {keys} list!",
    )


async def double_item_message(
    chat_id: id, context: ContextTypes, item: str, keys: str
) -> None:
    await message(
        chat_id,
        context,
        f"{item} is already in the {keys} list!",
    )


async def missing_item_message(
    chat_id: id, context: ContextTypes, item: str, keys: str
) -> None:
    await message(
        chat_id,
        context,
        f"{item} is not in the {keys} list!",
    )
