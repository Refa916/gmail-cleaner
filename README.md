# Gmail Cleaner

A Python script that connects to Gmail over IMAP, checks messages in a date range, and deletes emails whose subject contains configured keywords.

## What it does

- Logs into Gmail using IMAP
- Searches the inbox for messages in a selected date range
- Decodes and inspects email subjects
- Deletes emails that match spam or promotional keywords
- Saves progress so it can resume after interruptions

## Tech Stack

- Python
- Gmail IMAP
- `python-dotenv`

## Requirements

- Python 3
- Gmail account with IMAP enabled
- App password or account setup required by your Gmail security settings
- `python-dotenv` installed

Install the dependency:

```bash
python -m pip install python-dotenv
```

## Configuration

Create a `.env` file in the project root with:

```env
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-app-password
```

The script loads these values automatically.

## Customization

Open `main.py` to adjust:

- `keywords` list
- `SINCE` and `BEFORE` date range
- `BATCH_SIZE`
- `progress_file`

## Run

```bash
python main.py
```

## Warning

This script permanently deletes matching emails from the inbox. Review the keywords and date range carefully before running it in a production mail account.
