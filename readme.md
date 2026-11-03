# PROMOBOT

Automation system that monitors Amazon offers, filters them, generates marketing copy with OpenAI and publishes them to a Telegram channel.

## Flow

```
Offer Collector -> Filtering Engine -> OpenAI Copy Generator -> Telegram Publisher
```

## Features

- Offer collection (Amazon Creators API integration in progress)
- Configurable filtering (minimum discount, maximum price, allowed categories)
- Duplicate prevention with SQLite
- AI-generated sales copy with plain-text fallback
- Telegram channel publishing
- Async architecture with interval scheduler

## Tech Stack

Python, aiogram, OpenAI API, APScheduler, SQLite

## Configuration

Create a `.env` file with:

```
BOT_TOKEN=
CHANNEL_ID=
OPENAI_API_KEY=
OPENAI_MODEL=
SCHEDULER_INTERVAL_MINUTES=10
SEND_DELAY_SECONDS=3
```

## Usage

```
python main.py
python main.py --scheduler
```