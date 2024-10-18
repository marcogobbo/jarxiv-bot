# pylint: disable=C0116,C0114

import json
from pathlib import Path
from typing import Final

from telegram import Update
from telegram.ext import ContextTypes
from utils import (
    add_item_message,
    del_item_message,
    double_item_message,
    message,
    missing_item_message,
    no_config_message,
    no_item_message,
)

CONFIG_FOLDER: Final = "../../config/"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if not config_file.exists():
        default_config = {
            "chat": {
                "id": chat["id"],
                "type": chat["type"],
            },
            "keywords": [],
            "authors": [],
        }

        with open(config_file, "w", encoding="UTF-8") as file:
            json.dump(default_config, file, indent=4)

        await message(
            chat["id"],
            context,
            f"Configuration file created for the {chat['type']} chat <b>{chat['name']}</b> with ID <b>{chat['id']}</b>.",
        )
    else:
        await message(
            chat["id"],
            context,
            f"Configuration file for the {chat['type']} chat <b>{chat['name']}</b> with ID <b>{chat['id']}</b> already exists.",
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def action_item_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE, action: str, new_item: dict
) -> None:
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    try:
        with open(config_file, "r", encoding="UTF-8") as file:
            config = json.load(file)

    except FileNotFoundError:
        await no_config_message(chat, context)

        return

    key = next(iter(new_item))

    if not new_item[key]:
        await no_item_message(chat["id"], context, new_item)

        return

    item = new_item[key][0]
    keys = key + "s"

    if item in config[keys]:
        if action == "remove":

            getattr(config[keys], action)(item)

            with open(config_file, "w", encoding="UTF-8") as file:
                json.dump(config, file, indent=4)

            await del_item_message(chat["id"], context, item, keys)
        else:
            await double_item_message(chat["id"], context, item, keys)
    else:
        if action == "append":
            getattr(config[keys], action)(item)

            with open(config_file, "w", encoding="UTF-8") as file:
                json.dump(config, file, indent=4)

            await add_item_message(chat["id"], context, item, keys)
        else:
            await missing_item_message(chat["id"], context, item, keys)


async def add_author_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    action = "append"
    new_item = {"author": context.args}

    await action_item_command(update, context, action, new_item)


async def add_keyword_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    action = "append"
    new_item = {"keyword": context.args}

    await action_item_command(update, context, action, new_item)


async def del_author_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    action = "remove"
    new_item = {"author": context.args}

    await action_item_command(update, context, action, new_item)


async def del_keyword_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    action = "remove"
    new_item = {"keyword": context.args}

    await action_item_command(update, context, action, new_item)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    try:
        with open(config_file, "r", encoding="UTF-8") as file:
            config = json.load(file)

            if not config["authors"] and not config["keywords"]:
                await message(
                    chat["id"],
                    context,
                    "There are no authors and keywords in both lists!",
                )
                return

            response_text = ""

            if config["authors"]:
                authors = ", ".join(map(str, config["authors"]))
                response_text += f"<b>List of authors</b>: {authors}."
            else:
                response_text += "There are no authors in the authors list!"

            if config["keywords"]:
                keywords = ", ".join(map(str, config["keywords"]))
                response_text += f"\n<b>List of keywords</b>: {keywords}."
            else:
                response_text += "\nThere are no keywords in the keywords list!"

            await message(
                chat["id"],
                context,
                response_text,
            )

    except FileNotFoundError:
        await no_config_message(chat, context)
