# JarXiv Bot - A Telegram Bot for retrieving arXiv papers

**Jar**(vis)(ar)**Xiv Bot** is a Telegram bot that allows users to easily retrieve the latest academic papers from the arXiv repository by querying the **arXiv API**. Users can filter papers by specific authors or keywords found in titles and abstracts, making it an efficient tool for researchers to stay updated on relevant publications.

Current functions:
- `/start`: initialize the bot creating a configuration file in .json to store authors and keywords for private and group chats
- `/add_author` (`/aa`): add an author to the authors' list
- `/add_keyword` (`/ak`): add a keyword to the keywords' list
- `/del_author` (`/da`): delete an author from the authors' list
- `/del_keyword` (`/dk`): delete a keyword from the keywords' list
- `/list` (`/ls`): list both authors and keywords' list

## Prerequisites
- Python 3.11+ is required.
- Ensure you have `pip` or `poetry` installed.

## Installation
To install JarXiv Bot, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/marcogobbo/jarxiv-bot/
    ```

2. Install the bot:
    - For a normal installation, run:
        ```bash
        pip install .
        ```
    - To work in development mode (with `pre-commit` hooks):
        ```bash
        poetry install .
        pre-commit install
        ```

## License
JarXiv Bot is licensed under the [Apache License 2.0](https://github.com/marcogobbo/jarxiv-bot/blob/main/LICENSE).
