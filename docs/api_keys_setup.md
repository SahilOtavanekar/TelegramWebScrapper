# API Keys Setup Guide

To run the Telegram chatbot, you will need two new API keys: a **Telegram Bot Token** and a **Gemini API Key**. 
Here are the instructions on how to obtain and safely store them.

## 1. How to get a Telegram Bot Token
1. Open the Telegram app on your phone or desktop.
2. Search for the user **@BotFather** (it has a verified checkmark).
3. Start a chat and send the command `/newbot`.
4. Follow the prompts to name your bot and choose a unique username ending in `bot` (e.g., `MiamiPlumberLeadBot`).
5. Once created, **BotFather** will send you a message containing your **HTTP API Token** (it looks like a long string of numbers and letters).
6. Copy this token immediately.

## 2. How to get a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click the **Get API Key** button on the left sidebar (or navigate directly to the API Keys section).
4. Click **Create API Key**. You might need to link it to an existing Google Cloud Project, or let it create one for you.
5. Copy the generated API key immediately.

## 3. How to Store Your Keys Safely
**CRITICAL**: You should never commit these keys to source control (like GitHub). They must remain secret.

1. Open the `.env` file in the root directory of this project.
2. Add the following lines to your `.env` file, replacing the placeholder text with your actual copied keys:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

Your system is now configured to securely read these keys without exposing them to the public!
You can now run `execution/telegram_bot.py`.
