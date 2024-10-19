import os
from typing import Final

import pytz
from commands import add_author, add_keyword, del_author, del_keyword, list_items, start
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, Defaults

TOKEN: Final = os.getenv("JARXIV_BOT_TOKEN")
USERNAME: Final = "@jarxiv_bot"
CONFIG_FOLDER: Final = "../../config/"


if __name__ == "__main__":
    print("Starting bot...")
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone("Europe/Rome"))
    app = Application.builder().token(TOKEN).defaults(defaults).build()

    # Commands
    app.add_handler(CommandHandler(("start", "s"), start))
    app.add_handler(CommandHandler(("add_author", "aa"), add_author))
    app.add_handler(CommandHandler(("add_keyword" "ak"), add_keyword))
    app.add_handler(CommandHandler(("del_author", "da"), del_author))
    app.add_handler(CommandHandler(("del_keyword", "dk"), del_keyword))
    app.add_handler(CommandHandler(("list", "ls"), list_items))

    app.job_queue

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
