# Olx-parser-in-tg
“Telegram bot that fetches product details from OLX by link, compiles title, price and description into an Excel file, and tracks each user’s parse history in a SQLite database.”  — Aiogram framework — BeautifulSoup parsing — SQLAlchemy ORM
Below is a comprehensive English README.md for your Telegram OLX Parser Bot, including database integration via SQLAlchemy. I’ve structured it into clear sections with detailed explanations and code snippets.

Overview
This Telegram bot parses product listings from OLX upon receiving a link, stores parsed URLs and user info in a SQLite database via SQLAlchemy, and returns results as Excel files. It also tracks each user’s parse history.

Features
Link Parsing
The bot accepts OLX URLs, scrapes title, price, description, and links to product details.

Excel Export
Parsed data is saved to an .xlsx file and sent back to the user.

Persistent Storage
Uses SQLite + SQLAlchemy ORM to store users and parsed links.

Project Structure
olx-parser-bot/
├── bot.py                # Bot startup and dispatcher setup
├── app/
│   ├── handlers.py       # Telegram command & callback handlers
│   ├── parser.py         # OLX parsing logic
│   ├── history.py        # DB history functions
│   └── models.py         # SQLAlchemy ORM models & session
├── requirements.txt      # Python dependencies
├── db.sqlite3            # SQLite database file (auto‑created)
└── README.md             # This documentation
Installation
Clone the repository
