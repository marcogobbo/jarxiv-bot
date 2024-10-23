"""
This module provides utility functions for sending various types of messages
to Telegram chats. It includes generic message sending, messages related to
item management (e.g., authors or keywords), and status updates for
configuration files.
"""

from telegram.ext import ContextTypes


async def send_message(chat_id: int, context: ContextTypes, text: str) -> None:
    """
    Sends a message to a specified Telegram chat.

    Args:
        chat_id (int): The unique ID of the Telegram chat.
        context (telegram.ext.ContextTypes): Context object to access the bot and
                                             interact with Telegram.
        text (str): The message content to be sent to the chat.
    """
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
    )


async def item_message(
    chat_id: int, context: ContextTypes, item: str, keys: str, action: str
) -> None:
    """
    Sends a message to a Telegram chat indicating the status of an item (e.g., author or keyword)
    in relation to a list (added, removed, already exists, or missing).

    Args:
        chat_id (int): The unique ID of the Telegram chat.
        context (telegram.ext.ContextTypes): Context object to access the bot and interact
                                             with Telegram.
        item (str): The item (e.g., author, keyword) that the message refers to.
        keys (str): The name of the list the item belongs to (e.g., "authors" or "keywords").
        action (str): The action performed on the item (e.g., "append", "remove", "duplicate",
                      "missing").
    """
    # Define the message templates for different actions (add, remove, etc.).
    messages = {
        "append": (f"<b>{item}</b> has been added to the {keys} list!"),
        "remove": (f"<b>{item}</b> has been removed from the {keys} list!"),
        "duplicate": (f"<b>{item}</b> is already in the {keys} list!"),
        "missing": (f"<b>{item}</b> is not in the {keys} list!"),
    }

    # Send the appropriate message based on the action.
    await send_message(
        chat_id,
        context,
        messages[action],
    )


async def config_file_status(chat, context: ContextTypes, status: str) -> None:
    """
    Sends a message to a Telegram chat indicating the status of the configuration file
    (created, exists, missing, or error) for a specific chat.

    Args:
        chat (dict): A dictionary containing the chat details (id, type, name).
        context (telegram.ext.ContextTypes): Context object to access the bot and interact
                                             with Telegram.
        status (str): The status of the configuration file ("created", "exists", "missing",
                      or other errors).
    """
    # Determine the message content based on the status of the configuration file.
    if status == "created":
        message = (
            f"Configuration file created for the {chat['type']} chat "
            f"<b>{chat['name']}</b> with ID <b>{chat['id']}</b>."
        )
    elif status == "exists":
        message = (
            f"Configuration file for the {chat['type']} chat "
            f"<b>{chat['name']}</b> with ID <b>{chat['id']}</b> already exists."
        )
    elif status == "missing":
        message = (
            f"Configuration file not found for the {chat['type']} chat "
            f"<b>{chat['name']}</b> with ID <b>{chat['id']}</b>.\n"
            "Please initialize the configuration with <b>/start</b>."
        )
    else:
        message = (
            f"There is an issue with the configuration for the {chat['type']} chat "
            f"<b>{chat['name']}</b> with ID <b>{chat['id']}</b>."
        )

    # Send the configuration status message to the chat.
    await send_message(chat["id"], context, message)
