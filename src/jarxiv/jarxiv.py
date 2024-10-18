import os
from typing import Final

from commands import (
    add_author_command,
    add_keyword_command,
    del_author_command,
    del_keyword_command,
    list_command,
    start_command,
)
from telegram.ext import Application, CommandHandler

TOKEN: Final = os.getenv("JARXIV_BOT_TOKEN")
USERNAME: Final = "@jarxiv_bot"
CONFIG_FOLDER: Final = "../../config/"


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("add_author", add_author_command))
    app.add_handler(CommandHandler("add_keyword", add_keyword_command))
    app.add_handler(CommandHandler("del_author", del_author_command))
    app.add_handler(CommandHandler("del_keyword", del_keyword_command))
    app.add_handler(CommandHandler("list", list_command))

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
