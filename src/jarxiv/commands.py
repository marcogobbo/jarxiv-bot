"""
This module provides Telegram bot handlers to manage chat lists, such as adding/removing
authors and keywords, and scheduling daily message to send the latest submitted papers to
users or groups.
"""

import json
from datetime import time
from pathlib import Path
from typing import Final

from papers import send_papers
from telegram import Update
from telegram.ext import ContextTypes
from utils import config_file_status, item_message, send_message

# Path to the folder containing the configuration files for the bot.
CONFIG_FOLDER: Final = "../../config/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initializes or retrieves configuration for a chat and starts daily job scheduling.

    This function checks if a configuration file exists for the current chat. If not,
    it creates a default configuration file and schedules a daily job to send papers.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.

    Returns:
        None
    """
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if config_file.exists():
        # Notify that the configuration file already exists.
        await config_file_status(chat, context, "exists")
    else:
        # Create a new configuration file with default settings.
        default_config = {
            "chat": {
                "id": chat["id"],
                "type": chat["type"],
            },
            "keywords": [],
            "authors": [],
        }

        # Save the default configuration file.
        with open(config_file, "w", encoding="UTF-8") as file:
            json.dump(default_config, file, indent=4)

        # Notify that the configuration file has been created.
        await config_file_status(chat, context, "created")

    # Retrieve and initialize jobs for the current chat if none exist.
    current_jobs = context.job_queue.get_jobs_by_name(str(data.id))
    if not current_jobs:
        await init(data, context)


async def init(data, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Schedules a daily task for sending papers to the chat.

    Args:
        data (Chat): The chat data containing the chat ID.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for job scheduling.

    Returns:
        None
    """
    # Schedule a daily job to send papers to the chat.
    context.job_queue.run_daily(
        send_papers,
        time(hour=9, minute=00),
        chat_id=data.id,
        name=str(data.id),
        data=data,
    )


async def manage_item(
    update: Update, context: ContextTypes.DEFAULT_TYPE, action: str, new_item: dict
) -> None:
    """Manages adding or removing authors or keywords from the chat's list of authors or
    keywords.

    Depending on the action (append or remove), this function updates the chat's list
    of authors or keywords.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.
        action (str): The action to perform ('append' or 'remove').
        new_item (dict): A dictionary with the key ('author' or 'keyword') and value.

    Returns:
        None
    """
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if config_file.exists():
        # Load the configuration file if it exists.
        with open(config_file, encoding="UTF-8") as file:
            config = json.load(file)
    else:
        # Notify that the configuration file is missing.
        await config_file_status(chat, context, "missing")
        return

    key = next(iter(new_item))

    if not new_item[key]:
        # If no item is provided, request the name of the item.
        await send_message(
            chat["id"],
            context,
            f"Please specify the name of the {key}!",
        )
        return

    item = " ".join([str(x).lower() for x in new_item[key]])
    keys = key + "s"

    if item in config[keys]:
        if action == "remove":
            # Remove the item from the list.
            getattr(config[keys], action)(item)

            # Save the updated configuration.
            with open(config_file, "w", encoding="UTF-8") as file:
                json.dump(config, file, indent=4)

            await item_message(chat["id"], context, item, keys, action)
        else:
            # Item already exists, mark as duplicate.
            action = "duplicate"
            await item_message(chat["id"], context, item, keys, action)
    else:
        if action == "append":
            # Append the new item to the list.
            getattr(config[keys], action)(item)

            # Save the updated configuration.
            with open(config_file, "w", encoding="UTF-8") as file:
                json.dump(config, file, indent=4)

            await item_message(chat["id"], context, item, keys, action)
        else:
            # Item is missing from the list, notify the user.
            action = "missing"
            await item_message(chat["id"], context, item, keys, action)


async def add_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles adding a new author to the chat's author list.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.

    Returns:
        None
    """
    action = "append"
    new_item = {"author": context.args}
    await manage_item(update, context, action, new_item)


async def add_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles adding a new keyword to the chat's keyword list.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.

    Returns:
        None
    """
    action = "append"
    new_item = {"keyword": context.args}
    await manage_item(update, context, action, new_item)


async def del_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles removing an author from the chat's author list.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.

    Returns:
        None
    """
    action = "remove"
    new_item = {"author": context.args}
    await manage_item(update, context, action, new_item)


async def del_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles removing a keyword from the keyword list.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.

    Returns:
        None
    """
    action = "remove"
    new_item = {"keyword": context.args}
    await manage_item(update, context, action, new_item)


async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all authors and keywords of the current chat.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.

    Returns:
        None
    """
    chat_data = update.message.chat
    chat = {
        "id": chat_data.id,
        "type": chat_data.type,
        "name": chat_data.title or chat_data.username,
    }

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if config_file.exists():
        # Load the configuration file and retrieve authors and keywords.
        with open(config_file, encoding="UTF-8") as file:
            config = json.load(file)

        message = []
        items = {
            "authors": config.get("authors", []),
            "keywords": config.get("keywords", []),
        }

        if not items["authors"] and not items["keywords"]:
            # Notify if both lists are empty.
            await send_message(
                chat["id"],
                context,
                "There are no authors and keywords in both lists!",
            )
            return

        # Construct the message listing the authors and keywords.
        for item_name, item_list in items.items():
            if item_list:
                item_list_str = ", ".join(map(str, item_list))
                message.append(f"<b>List of {item_name}</b>: {item_list_str}.")
            else:
                message.append(f"There are no {item_name} in the {item_name} list!")

        await send_message(chat["id"], context, "\n".join(message))
    else:
        # Notify that the configuration file is missing.
        await config_file_status(chat, context, "missing")


async def get_latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Retrieves and sends the latest papers to the chat.

    Args:
        update (Update): The update containing the chat information.
        context (ContextTypes.DEFAULT_TYPE): Contextual information for the bot's handler.

    Returns:
        None
    """
    data = update.message.chat
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    if config_file.exists():
        # Retrieves and send the latest papers.
        await send_papers(context, data)
    else:
        # Notify that the configuration file is missing.
        await config_file_status(chat, context, "missing")
        return
