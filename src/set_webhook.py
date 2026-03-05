import os
import sys
import telebot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    print("TELEGRAM_BOT_TOKEN not found in .env")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python set_webhook.py <WEBHOOK_URL>")
    print("Example: python set_webhook.py https://my-username--telegram-lead-bot-webhook.modal.run")
    sys.exit(1)

webhook_url = sys.argv[1]

print(f"Connecting to Telegram API...")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

print(f"Setting webhook to: {webhook_url}")
success = bot.set_webhook(url=webhook_url)

if success:
    print("Webhook successfully set!")
    print("Telegram will now forward messages directly to your Modal endpoint.")
else:
    print("Failed to set webhook. Please verify your token and URL.")
