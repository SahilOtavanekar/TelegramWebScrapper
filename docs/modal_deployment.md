# Modal Deployment Guide

This guide explains how to take the Telegram Lead Scraper bot from your local machine and deploy it to the cloud using [Modal.com](https://modal.com/).

## 1. Setup Modal Account
If you haven't already:
1. Create an account at [modal.com](https://modal.com/).
2. Run `modal setup` in your terminal to authenticate your machine.

## 2. Store Your Secrets Safely
Instead of relying on the local `.env` file, Modal uses Secret objects stored securely in their cloud.
We need to create a Secret named `telegram-bot-secrets` containing your 5 configuration variables.

Run the following command in your terminal, replacing the dummy values with your actual keys from your `.env` file:
```bash
modal secret create telegram-bot-secrets \
    TELEGRAM_BOT_TOKEN="your_telegram_token" \
    GEMINI_API_KEY="your_gemini_key" \
    AIRTABLE_API_KEY="your_airtable_key" \
    AIRTABLE_BASE_ID="your_base_id" \
    AIRTABLE_TABLE_NAME="your_table_name"
```

## 3. Deploy to Modal
Once your secrets are saved, you can deploy the webhook server. Run:
```bash
modal deploy execution/modal_bot.py
```

## 4. Set the Webhook URL
When the deployment finishes, Modal will output a URL that looks like `https://your-username--telegram-lead-bot-webhook.modal.run`.

Telegram needs to know this URL so it can push new messages to your Modal app.
You can set this automatically by running a local helper script:
```bash
python execution/set_webhook.py https://your-username--telegram-lead-bot-webhook.modal.run
```

Your bot is now live in the cloud! It will spin up instantly when someone messages it and shut down when idle, costing $0 while unused.
