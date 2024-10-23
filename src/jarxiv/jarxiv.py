"""
This module initializes and runs a Telegram bot for managing chat's list of authors or
keywords, such as adding/removing authors and keywords, and scheduling daily message to
send the latest submitted papers to users or groups.
"""

import os
from typing import Final

import pytz
from commands import add_author, add_keyword, del_author, del_keyword, list_items, start
from telegram import LinkPreviewOptions
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, Defaults

# Retrieve the bot token environment variable, bot username and config folder file path.
TOKEN: Final = os.getenv("JARXIV_BOT_TOKEN")
USERNAME: Final = "@jarxiv_bot"
CONFIG_FOLDER: Final = "../../config/"

# Disable link previews in messages sent by the bot.
link_preview_options = LinkPreviewOptions(is_disabled=True)

if __name__ == "__main__":
    print("Starting bot...")

    # Set default options for the bot.
    defaults = Defaults(
        parse_mode=ParseMode.HTML,
        tzinfo=pytz.timezone("Europe/Rome"),
        link_preview_options=link_preview_options,
    )

    # Create the Application instance with the token and defaults.
    app = Application.builder().token(TOKEN).defaults(defaults).build()

    # Add command handlers for bot commands.
    app.add_handler(CommandHandler(("start"), start))
    app.add_handler(CommandHandler(("add_author", "aa"), add_author))
    app.add_handler(CommandHandler(("add_keyword", "ak"), add_keyword))
    app.add_handler(CommandHandler(("del_author", "da"), del_author))
    app.add_handler(CommandHandler(("del_keyword", "dk"), del_keyword))
    app.add_handler(CommandHandler(("list", "ls"), list_items))

    # Start polling for new updates with a poll interval of 3 seconds.
    print("Polling...")
    app.run_polling(poll_interval=3)
