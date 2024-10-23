# JarXiv Bot - A Telegram Bot for arXiv papers
![Python Version](https://img.shields.io/badge/python-3.11+-blue)
![GitHub Release](https://img.shields.io/github/v/release/marcogobbo/jarxiv-bot)
![GitHub License](https://img.shields.io/github/license/marcogobbo/jarxiv-bot)

🤖 **Jar**(vis)(ar)**Xiv Bot** is a Telegram bot that allows users to easily retrieve the latest academic papers from the [arXiv](https://arxiv.org/) repository by querying the arXiv API using [arxiv.py](https://github.com/lukasschwab/arxiv.py). Users can filter papers by specific authors or keywords found in titles and abstracts, making it an efficient tool for researchers to stay updated on relevant publications.

JarXiv Bot provides the following commands:

- `/start`: initializes the bot and creates a configuration file (`.json`) to store author and keyword preferences for both private and group chats.
- `/add_author` (`/aa`): adds an author to the author list.
- `/add_keyword` (`/ak`): adds a keyword to the keyword list.
- `/del_author` (`/da`): removes an author from the author list.
- `/del_keyword` (`/dk`): removes a keyword from the keyword list.
- `/list` (`/ls`): displays both the author and keyword lists.

## Prerequisites
- Python 3.11+ is required.
- Ensure you have `pip` or `poetry` installed.

## Installation
To install JarXiv Bot, follow these steps:

```bash
git clone https://github.com/marcogobbo/jarxiv-bot/
pip install .
```

## Development
To work in development mode (with `pre-commit` hooks):
```bash
git clone https://github.com/marcogobbo/jarxiv-bot/
poetry install .
pre-commit install
```

## License
JarXiv Bot is licensed under the [Apache License 2.0](https://github.com/marcogobbo/jarxiv-bot/blob/main/LICENSE).
