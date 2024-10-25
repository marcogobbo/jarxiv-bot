"""
This module is responsible for fetching and sending the latest arXiv papers
based on chat-specific configurations, such as author names and keywords.
It queries the arXiv API using these filters and sends the results to the
Telegram chat.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Final

import arxiv
from telegram.ext import ContextTypes

# Path to the folder containing the configuration files for the bot.
CONFIG_FOLDER: Final = "../../config/"


async def send_papers(context: ContextTypes) -> None:
    """
    Fetches and sends the latest submitted arXiv papers to a Telegram chat based on
    configured authors and keywords stored in a JSON file. If no new papers match the
    query, it notifies the chat that no papers were found.

    Args:
        context (telegram.ext.ContextTypes): Context object from Telegram containing
                                             job data and bot interaction details.
    """
    # Retrieve job-specific data, including the chat ID and type.
    data = context.job.data
    chat = {"id": data.id, "type": data.type, "name": data.title or data.username}

    # Construct the path to the chat-specific configuration file.
    config_file = Path(f"{CONFIG_FOLDER}/{chat['type']}/{chat['id']}_config.json")

    # Load the chat configuration (authors and keywords) from the JSON file.
    with open(config_file, encoding="UTF-8") as file:
        config = json.load(file)

    # If there are no authors or keywords in the config, exit the function.
    if not config["authors"] and not config["keywords"]:
        return

    # Construct the search query for authors and keywords.
    authors_query = (
        " OR ".join(f'au:"{author}"' for author in config["authors"])
        if config["authors"]
        else ""
    )
    keywords_query = (
        " OR ".join(
            f'ti:"{keyword}" OR abs:"{keyword}"' for keyword in config["keywords"]
        )
        if config["keywords"]
        else ""
    )
    query = f"{authors_query} OR {keywords_query}".strip(" OR ")

    # Create an arXiv client to execute the search query.
    client = arxiv.Client()

    # Search for the latest 10 papers using the constructed query, sorted by submission date.
    result = arxiv.Search(
        query=query, max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate
    )

    # Convert the search result into a list of paper objects.
    papers = list(client.results(result))

    # If no papers are found, notify the chat and stop.
    if not papers:
        await context.bot.send_message(
            chat["id"], "No new papers found.", disable_web_page_preview=True
        )
        return

    # Prepare the message to send, starting with a header.
    message = [
        f"Last submitted {len(papers)} papers for {datetime.today().strftime('%d-%m-%Y')}\n"
    ]

    # Add details of each paper to the message.
    for idx, paper in enumerate(papers):
        message.append(
            f'<b>{idx + 1}. <a href="{paper.links[0]}">{paper.title}</a></b> - '
            f"{paper.authors[0]} et al. ({paper.published.strftime('%d-%m-%Y')})"
        )

    # Send the message to the chat with the list of papers, disabling web page previews.
    await context.bot.send_message(chat["id"], "\n".join(message))
