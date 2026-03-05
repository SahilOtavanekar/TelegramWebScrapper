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

The bot uses **Google Gemini's function-calling API** to understand intent, spins up a **headless Playwright browser** in the cloud to scrape Google Maps, and saves the results directly to **Airtable** as a structured CRM database.

Built on **Modal's serverless infrastructure**, there are no always-on servers — you pay only for what you use.

---

## ✨ Features

- 🗣️ **Natural Language Interface** — No commands to memorize; just chat naturally
- 🔍 **Google Maps Scraping** — Headless browser extracts name, address, website, rating, and more
- 🧠 **AI Intent Routing** — Gemini automatically decides whether to scrape, query, or chat
- 🗃️ **Airtable CRM Integration** — All leads bulk-uploaded and queryable with filters (city, rating, status)
- ☁️ **100% Serverless** — Hosted on Modal with zero idle cost and automatic scaling
- ⚡ **Async Architecture** — Webhook responds instantly; scraping runs as a long-lived background task
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
├── tests/
│   ├── test_models.py
│   ├── test_parse.py
│   ├── test_scrape_and_save.py
│   ├── test_secrets_modal.py
│   └── test_webhook.py
├── docs/
│   ├── api_keys_setup.md      # How to get all required API keys
│   ├── airtable_setup.md      # Airtable base/table configuration
│   ├── modal_deployment.md    # Modal deployment walkthrough
│   ├── airtable_save_leads.md
│   ├── airtable_pull_leads.md
│   └── scrape_google_maps.md
├── .env.example               # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A [Modal](https://modal.com) account
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

Open `.env` and fill in your values (see [Environment Variables](#-environment-variables) below).

### 3. Deploy to Modal

```bash
# Upload your secrets securely to Modal
modal secret create telegram-bot-secrets .env

# Deploy the serverless app
modal deploy src/modal_bot.py
```

Modal will print a webhook URL like:
```
https://your-username--telegram-lead-bot-webhook.modal.run
```

### 4. Register the Telegram Webhook

```bash
python src/set_webhook.py https://your-username--telegram-lead-bot-webhook.modal.run
```

Your bot is now live! Open Telegram and start chatting. 🎉

---

## 🔑 Environment Variables

| Variable | Description | Where to Get It |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Your Telegram Bot token | [@BotFather](https://t.me/BotFather) |
| `GEMINI_API_KEY` | Google Gemini API key | [AI Studio](https://aistudio.google.com/app/apikey) |
| `AIRTABLE_API_KEY` | Airtable Personal Access Token | [Airtable Tokens](https://airtable.com/create/tokens) |
| `AIRTABLE_BASE_ID` | ID of your Airtable Base (`appXXXXX`) | Base URL in Airtable |
| `AIRTABLE_TABLE_NAME` | ID or name of the leads table | Airtable UI |

> See [`docs/api_keys_setup.md`](docs/api_keys_setup.md) for a detailed step-by-step guide.

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

## 📊 Example Output

```
✅ Successfully scraped 5 leads and saved 5 to Airtable!

**Top Scraped Leads:**
1. Blue Bottle Coffee (4.6 stars) - 300 S Grand Ave, Los Angeles
2. Intelligentsia Coffee (4.5 stars) - 3922 Sunset Blvd, Los Angeles
3. Verve Coffee Roasters (4.7 stars) - 833 S Spring St, Los Angeles
```

---

## 🔄 Execution Flow

```
User sends message
        │
        ▼
Telegram → Modal Webhook (immediate 200 OK)
        │
        ▼ (background)
Gemini analyzes intent
        │
   ┌────┴────┐
   ▼         ▼
Scrape     Query
Google     Airtable
Maps       (existing
        leads)
   │         │
   └────┬────┘
        ▼
Bot sends reply to Telegram
```

1. **Instant Response**: The webhook returns `200 OK` immediately to prevent Telegram timeouts
2. **Background Processing**: A Modal function handles the heavy lifting (up to 10 minutes)
3. **AI Routing**: Gemini decides which tool to call based on natural language
4. **Result Delivery**: The bot pushes the formatted response back to the user via Telegram API

---

## 🛠️ Local Development

For rapid iteration without deploying to Modal, use the local polling bot:

```bash
# Ensure .env is configured
python src/telegram_bot.py
```

This runs the bot in long-polling mode on your local machine using the same Gemini + Airtable integrations.

---

## 📚 Documentation

| Document | Description |
|---|---|
| [`docs/api_keys_setup.md`](docs/api_keys_setup.md) | How to obtain all required API keys |
| [`docs/airtable_setup.md`](docs/airtable_setup.md) | Setting up your Airtable base and table |
| [`docs/modal_deployment.md`](docs/modal_deployment.md) | Full Modal deployment walkthrough |
| [`docs/scrape_google_maps.md`](docs/scrape_google_maps.md) | Scraper internals and configuration |
| [`docs/airtable_save_leads.md`](docs/airtable_save_leads.md) | Lead upload and field mapping |
| [`docs/airtable_pull_leads.md`](docs/airtable_pull_leads.md) | Query filters and result format |

---

## ⚙️ Technical Highlights

- **LLM Tool Calling**: Gemini's native `tools=` API eliminates the need for regex parsing — the model handles argument formatting from natural language automatically
- **Async Webhook Architecture**: Solves Telegram's 15-second response limit by separating the fast webhook endpoint from the long-running scraping task
- **Headless Resilience**: Handles EU cookie/consent dialogs, infinite scroll, and direct single-place page redirects from Google Maps
- **Secrets Management**: All API keys are injected via Modal Secrets at runtime — never stored in the container image or code

---

## 📄 License

This project is licensed under the MIT License.
