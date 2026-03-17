# 🤖 Telegram Lead Generation Bot

> An AI-powered, serverless Telegram chatbot that scrapes Google Maps for business leads and manages them in Airtable — all through natural language conversation.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Modal](https://img.shields.io/badge/Serverless-Modal-6C47FF?style=flat)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4?style=flat&logo=google&logoColor=white)
![Playwright](https://img.shields.io/badge/Scraping-Playwright-2EAD33?style=flat&logo=playwright&logoColor=white)
![Airtable](https://img.shields.io/badge/Database-Airtable-18BFFF?style=flat&logo=airtable&logoColor=white)

---

## 📖 Overview

Instead of rigid commands like `/scrape city service`, this bot lets you simply *chat* with it:

> *"Find me 10 coffee shops in downtown Toronto and save them"*
> *"Show me plumbers in Mumbai rated above 4 stars"*

The bot uses **Google Gemini's function-calling API** to understand intent, spins up a **headless Playwright browser** (locally or via Modal) to scrape Google Maps, and saves the results directly to **Airtable** as a structured CRM database.

Built to be **100% Serverless** on Modal, or run locally for development.

---

## ✨ Features

- 🗣️ **Natural Language Interface** — No commands to memorize; just chat naturally
- 🔍 **Google Maps Scraping** — Headless browser extracts name, address, website, rating, and more
- 🧠 **AI Intent Routing** — Gemini automatically decides whether to scrape, query, or chat
- 🗃️ **Airtable CRM Integration** — All leads bulk-uploaded and queryable with filters (city, rating, status)
- ☁️ **Cloud Ready** — Hosted on Modal with zero idle cost and automatic scaling
- ⚡ **Async Architecture** — Webhook responds instantly; scraping runs as a background task
- 🛡️ **Consent Bypass** — Handles EU cookie/consent dialogs from headless browsers automatically

---

## 🏗️ Architecture

```
┌─────────────┐     webhook POST      ┌──────────────────────────┐
│  Telegram   │ ──────────────────► │  Modal Fast Endpoint     │
│   (User)    │ ◄──────────────────  │  (FastAPI, instant 200)  │
└─────────────┘   bot.send_message   └──────────┬───────────────┘
                                                │ .spawn()
                                                ▼
                                   ┌────────────────────────────┐
                                   │  Modal Background Function │
                                   │  (up to 10 min timeout)    │
                                   │                            │
                                   │  ┌──────────────────────┐  │
                                   │  │  Google Gemini       │  │
                                   │  │  (Intent Analysis +  │  │
                                   │  │   Tool Calling)      │  │
                                   │  └────────┬─────────────┘  │
                                   │           │                 │
                                   │     ┌─────┴──────┐         │
                                   │     ▼            ▼         │
                                   │  Playwright   Airtable     │
                                   │  (Scraper)    (Query/Save) │
                                   └────────────────────────────┘
```

---

## 📁 Project Structure

```
telegram-lead-bot/
├── src/
│   ├── modal_bot.py           # Serverless entry point (Modal app + webhook)
│   ├── telegram_bot.py        # Local polling bot (for development)
│   ├── scrape_google_maps.py  # Playwright scraping engine
│   ├── airtable_save_leads.py # Airtable write operations
│   ├── airtable_pull_leads.py # Airtable read/query operations
│   └── set_webhook.py         # Utility: register Telegram webhook URL
├── .env.example               # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A [Modal](https://modal.com) account (optional for local run)
- A [Telegram Bot](https://core.telegram.org/bots#botfather) token
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key
- An [Airtable](https://airtable.com) base with a configured table

### 1. Clone & Install

```bash
git clone https://github.com/your-username/telegram-lead-bot.git
cd telegram-lead-bot

python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values.

### 3. Running Locally
For rapid iteration, use the local polling bot:
```bash
python src/telegram_bot.py
```

### 4. Deploy to Modal (Cloud Hosting)

```bash
# Upload your secrets securely to Modal
modal secret create telegram-bot-secrets .env

# Deploy the serverless app
modal deploy src/modal_bot.py

# Modal will print a webhook URL. Use it to set the Telegram webhook:
python src/set_webhook.py YOUR_MODAL_WEBHOOK_URL
```

---

## 🔑 Environment Variables

| Variable | Description | Where to Get It |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram Bot token | [@BotFather](https://t.me/BotFather) |
| `GEMINI_API_KEY` | Google Gemini API key | [AI Studio](https://aistudio.google.com/app/apikey) |
| `AIRTABLE_API_KEY` | Airtable Personal Access Token | [Airtable Tokens](https://airtable.com/create/tokens) |
| `AIRTABLE_BASE_ID` | ID of your Airtable Base (`appXXXXX`) | Base URL in Airtable |
| `AIRTABLE_TABLE_NAME` | ID or name of the leads table | Airtable UI |

---

## 💬 Usage Examples

| User Message | Bot Action |
|---|---|
| *"Find 5 plumbers in Mumbai"* | Scrapes Google Maps → saves to Airtable |
| *"Get me 10 coffee shops in Toronto"* | Scrapes Google Maps → saves to Airtable |
| *"Show me leads in Kandivali"* | Queries Airtable, returns existing leads |
| *"Any plumbers rated above 4 stars?"* | Queries Airtable with rating filter |
| *"What can you do?"* | Conversational reply from Gemini |

---

## ⚙️ Technical Highlights

- **LLM Tool Calling**: Gemini's native `tools=` API eliminates the need for regex parsing — the model handles argument formatting from natural language automatically.
- **Async Webhook Architecture**: Solves Telegram's 15-second response limit on Modal by separating the fast webhook endpoint from the long-running scraping task.
- **Headless Resilience**: Handles EU cookie/consent dialogs, infinite scroll, and direct single-place page redirects from Google Maps via Playwright.

---

## 📄 License

This project is licensed under the MIT License.
