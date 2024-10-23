# JarXiv Bot

**Jar**(vis)(Ar)**Xiv Bot** is a Telegram Bot developed to retrieve the last submitted papers querying the **ArXiv API** selecting for authors and keywords (searching the keyword in the title and abstract).
Current functions:
- `/start`: initialize the bot creating a configuration file in .json to store authors and keywords for private and group chats
- `/add_author` (`/aa`): add an author to the authors' list
- `/add_keyword` (`/ak`): add a keyword to the keywords' list
- `/del_author` (`/da`): delete an author from the authors' list
- `/del_keyword` (`/dk`): delete a keyword from the keywords' list
- `/list` (`/ls`): list both authors and keywords' list

## Installation
Clone the repository with

```bash
git clone https://github.com/marcogobbo/jarxiv-bot/
```

Install it in normal mode

```bash
pip install .
```

or if you want to work in developer mode

```bash
poetry install .
pre-commit install
```

## Author
- [@marcogobbo](https://github.com/marcogobbo/)

## License
JarXiv Bot is licensed under the [Apache License 2.0](https://github.com/marcogobbo/jarxiv-bot/blob/main/LICENSE).
