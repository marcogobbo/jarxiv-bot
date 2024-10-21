# pylint: disable=C0116,C0114
import json
from datetime import datetime
from pathlib import Path
from typing import Final

import arxiv
from telegram.ext import ContextTypes

CONFIG_FOLDER: Final = "../../config/"


async def send_papers(context: ContextTypes) -> None:
    data = context.job.data
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}
    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    with open(config_file, encoding="UTF-8") as file:
        config = json.load(file)

    authors = config["authors"]
    keywords = config["keywords"]

    if not config["authors"] and not config["keywords"]:
        return

    authors_query = " OR ".join(f"au:{author}" for author in authors) if authors else ""
    keywords_query = (
        " OR ".join(f"ti:{keyword} OR abs:{keyword}" for keyword in keywords)
        if keywords
        else ""
    )
    query = f"{authors_query} OR {keywords_query}".strip(" OR ")

    client = arxiv.Client()

    result = arxiv.Search(
        query=query, max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = list(client.results(result))

    if not papers:
        await context.bot.send_message(
            chat["id"], "No new papers found.", disable_web_page_preview=True
        )
        return

    message = [
        f"Last submitted {len(papers)} papers for {datetime.today().strftime('%d-%m-%Y')}\n"
    ]

    for idx, paper in enumerate(papers):
        message.append(
            f"<b>{idx + 1}. <a href=\"{paper.links[0]}\">{paper.title}</a></b> - {paper.authors[0]} et al. ({paper.published.strftime('%d-%m-%Y')})"
        )

    await context.bot.send_message(
        chat["id"], "\n".join(message), disable_web_page_preview=True
    )
