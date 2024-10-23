# pylint: disable=C0116,C0114

import json
from datetime import time
from pathlib import Path
from typing import Final

from papers import send_papers
from telegram import Update
from telegram.ext import ContextTypes
from utils import config_file_status, item_message, send_message

CONFIG_FOLDER: Final = "../../config/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if config_file.exists():
        await config_file_status(chat, context, "exists")

    else:
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

        await config_file_status(chat, context, "created")

    current_jobs = context.job_queue.get_jobs_by_name(str(data.id))

    if not current_jobs:
        await init(data, context)


async def init(data, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.job_queue.run_daily(
        send_papers,
        time(hour=16, minute=00),
        chat_id=data.id,
        name=str(data.id),
        data=data,
    )


async def manage_item(
    update: Update, context: ContextTypes.DEFAULT_TYPE, action: str, new_item: dict
) -> None:
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if config_file.exists():
        with open(config_file, encoding="UTF-8") as file:
            config = json.load(file)

    else:
        await config_file_status(chat, context, "missing")

        return

    key = next(iter(new_item))

    if not new_item[key]:
        await send_message(
            chat["id"],
            context,
            f"Please specify the name of the {key}!",
        )

        return

    item = " ".join(new_item[key])
    keys = key + "s"

    if item in config[keys]:
        if action == "remove":
            getattr(config[keys], action)(item)

            with open(config_file, "w", encoding="UTF-8") as file:
                json.dump(config, file, indent=4)

            await item_message(chat["id"], context, item, keys, action)
        else:
            action = "duplicate"
            await item_message(chat["id"], context, item, keys, action)
    else:
        if action == "append":
            getattr(config[keys], action)(item)

            with open(config_file, "w", encoding="UTF-8") as file:
                json.dump(config, file, indent=4)

            await item_message(chat["id"], context, item, keys, action)
        else:
            action = "missing"
            await item_message(chat["id"], context, item, keys, action)


async def add_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    action = "append"
    new_item = {"author": context.args}

    await manage_item(update, context, action, new_item)


async def add_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    action = "append"
    new_item = {"keyword": context.args}
    await manage_item(update, context, action, new_item)


async def del_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    action = "remove"
    new_item = {"author": context.args}

    await manage_item(update, context, action, new_item)


async def del_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    action = "remove"
    new_item = {"keyword": context.args}

    await manage_item(update, context, action, new_item)


async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_data = update.message.chat
    chat = {
        "id": chat_data.id,
        "type": chat_data.type,
        "name": chat_data.title or chat_data.username,
    }

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if config_file.exists():
        with open(config_file, encoding="UTF-8") as file:
            config = json.load(file)

        message = []
        items = {
            "authors": config.get("authors", []),
            "keywords": config.get("keywords", []),
        }

        if not items["authors"] and not items["keywords"]:
            await send_message(
                chat["id"],
                context,
                "There are no authors and keywords in both lists!",
            )
            return

        for item_name, item_list in items.items():
            if item_list:
                item_list_str = ", ".join(map(str, item_list))
                message.append(f"<b>List of {item_name}</b>: {item_list_str}.")
            else:
                message.append(f"There are no {item_name} in the {item_name} list!")

        await send_message(chat["id"], context, "\n".join(message))

    else:
        await config_file_status(chat, context, "missing")
