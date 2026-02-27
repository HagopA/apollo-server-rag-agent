# Apollo Bot

A RAG-powered AI support chatbot for your private Plex media server, built with Discord.

Apollo Bot answers user questions using your documentation, and can check real-time data from your media services via LLM tool use.

> **Note:** "Apollo" is the name of my server. Throughout the code and docs, you'll see references to "Apollo" — treat these as placeholders for your own server name. The bot name is configurable via the `BOT_NAME` environment variable.

## Features

- **RAG-powered answers** — Answers questions from your documentation using ChromaDB vector search
- **Live service integration** — Checks real-time request status, download queues, and Plex activity
- **Discord threads** — Automatically creates threads to keep conversations organized
- **Rate limiting** — Per-user rate limits to control API costs
- **Conversation memory** — Maintains context within threads for follow-up questions
- **Admin commands** — Re-ingest docs on the fly with `!ingest`

## Architecture

```
User (Discord)
    |
bot.py (Discord listener + thread management)
    |
llm.py (LLM API + tool orchestration)
    |-- rag.py -> ChromaDB (document retrieval)
    +-- tools/ -> Media Request / Movie / TV / Activity APIs
    |
Response -> Discord
```

---

## Setup Guide

### Prerequisites

- **Python 3.11 or 3.12** — [Download here](https://www.python.org/downloads/). During installation, check "Add Python to PATH".
- **Git** — [Download here](https://git-scm.com/download/win)
- **Docker** (for deployment) — [Download here](https://www.docker.com/products/docker-desktop/)

Verify Python is installed:

```
python --version
```

---

### Step 1. Create a Discord Bot

1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it (e.g., "Apollo Assistant") → click **Create**
3. In the left sidebar, click **Bot**
4. Click **Reset Token** → confirm → **copy the token immediately** (you won't see it again). This goes in your `.env` file as `DISCORD_BOT_TOKEN`.
5. Scroll down to **Privileged Gateway Intents** and enable:
   - **Message Content Intent** (required for the bot to read messages)
6. In the left sidebar, click **OAuth2** → **URL Generator**
7. Under **Scopes**, check: `bot`
8. Under **Bot Permissions**, check:
   - `Send Messages`
   - `Create Public Threads`
   - `Send Messages in Threads`
   - `Read Message History`
9. Copy the **Generated URL** at the bottom of the page
10. Paste the URL into your browser → select your Discord server → **Authorize**

The bot will appear in your server (offline until you run the code).

Create a channel for the bot (e.g., `#ask-apollo`). Right-click the channel → **Copy Channel ID**. (If you don't see this option, go to Discord Settings → Advanced → enable **Developer Mode**.) This goes in your `.env` as `DISCORD_CHANNEL_ID`.

---

### Step 2. Get Your API Keys

You need API keys from each service:

| Service      | How to get the key |
|--------------|-------------------|
| **LLM API** | Go to your LLM provider's console → Create a new API key. You'll need to add credit ($5 minimum). This is a pay-as-you-go API — see cost estimate below. |
| **Media Requests** | Open the media request service web UI → **Settings** → **General** → scroll to **API Key** → copy it |
| **Movie Service**  | Open the movie service web UI → **Settings** → **General** → **Security** section → **API Key** |
| **TV Service**     | Open the TV service web UI → **Settings** → **General** → **Security** section → **API Key** |
| **Activity Monitor** | Open the activity monitor web UI → **Settings** → **Web Interface** → **API Key** |

---

### Step 3. Clone and Install

```bash
git clone https://github.com/HagopA/apollo-server-rag-agent.git
cd apollo-server-rag-agent

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

### Step 4. Configure Environment Variables

1. Copy `.env.example` to `.env`
2. Fill in your values:

```env
# --- Discord ---
DISCORD_BOT_TOKEN=paste_your_discord_bot_token_here
DISCORD_CHANNEL_ID=paste_your_channel_id_here

# --- LLM API ---
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# --- Media Requests ---
MEDIA_REQUESTS_URL=http://your-server-ip:5055
MEDIA_REQUESTS_API_KEY=paste_media_requests_key_here

# --- Movie Service ---
MOVIE_SERVICE_URL=http://your-server-ip:7878
MOVIE_SERVICE_API_KEY=paste_movie_service_key_here

# --- TV Service ---
TV_SERVICE_URL=http://your-server-ip:8989
TV_SERVICE_API_KEY=paste_tv_service_key_here

# --- Activity Monitor ---
ACTIVITY_SERVICE_URL=http://your-server-ip:8181
ACTIVITY_SERVICE_API_KEY=paste_activity_service_key_here
```

Replace `your-server-ip` with the IP or hostname of your media server. The port numbers should match your service configurations.

---

### Step 5. Add Your Documentation

The `docs/` folder is the bot's knowledge base. Every `.md` file in this folder gets chunked and embedded into a vector database so the bot can search through it when answering questions.

Sample documentation files are included. Edit them to match your setup, or add new ones.

**Recommended doc files:**

| File | Contents |
|------|----------|
| `docs/user-guide.md` | General user guide for your media server setup |
| `docs/requesting.md` | Walkthrough of how to request media |
| `docs/troubleshooting.md` | Common problems and solutions |
| `docs/faq.md` | Frequently asked questions |
| `docs/server-rules.md` | Request limits, content policies, etc. |
| `docs/anime.md` | Anime-specific info (dual audio, subgroups, etc.) |

**Tips for writing good docs:**
- Write them as if you're explaining to a user, not as technical notes.
- Use `## Headings` to organize sections — the RAG chunker splits on these headings, so each section becomes a retrievable chunk.
- Be specific. "Movies download in up to 4K HDR" is better than "we get good quality."
- The more docs you add, the better the bot's answers. You can always add more later and run `!ingest` to reload.

---

### Step 6. Test Locally

**6a. Ingest your documentation:**

```
python ingest.py
```

Expected output:

```
Ingesting documentation from ./docs/
  user-guide.md: 8 chunks
Ingested 8 chunks from 1 files.
```

**6b. Test retrieval:**

```
python ingest.py query "how do I request a movie"
```

This searches your docs and shows the most relevant chunks. If you get results, RAG is working.

**6c. Run the bot:**

```
python bot.py
```

Expected output:

```
Starting Apollo Assistant...
INFO     apollo-bot: Apollo Assistant is online as ApolloAssistant#1234
INFO     apollo-bot:    Listening in channel ID: 123456789
```

**6d. Test in Discord:**

Go to your bot's channel and try:
- `!status` — Should confirm the bot is online
- `How do I request a movie?` — Should create a thread and answer from your docs
- `What's currently downloading?` — Should query the movie/TV service APIs and report status
- `Check the status of Oppenheimer` — Should search the media request service for that title

**Troubleshooting:**
- **"DISCORD_BOT_TOKEN is not set"** → Your `.env` file isn't being found. Make sure it's named exactly `.env` (not `.env.txt`) and is in the project root.
- **Connection errors to media services** → Your machine can't reach the service URLs. Check the URLs in `.env` and test them in your browser.
- **LLM API errors** → Check that your API key is correct and that you've added credit to your account.
- **"ModuleNotFoundError"** → Dependencies aren't installed. Make sure your virtual environment is activated and re-run `pip install -r requirements.txt`.

---

### Step 7. Deploy with Docker

Once everything works locally, deploy with Docker for 24/7 operation.

**7a. Configure `.env` URLs for deployment:**

If deploying on the same machine as your media services with `network_mode: host`:

```env
MEDIA_REQUESTS_URL=http://localhost:5055
MOVIE_SERVICE_URL=http://localhost:7878
TV_SERVICE_URL=http://localhost:8989
ACTIVITY_SERVICE_URL=http://localhost:8181
```

**7b. Build and start:**

```bash
docker compose up -d --build
```

**7c. Check that it's running:**

```bash
docker logs apollo-bot
```

**7d. Useful commands:**

```bash
docker logs apollo-bot --tail 50     # View last 50 log lines
docker logs apollo-bot -f            # Follow logs in real-time (Ctrl+C to exit)
docker compose restart               # Restart the bot
docker compose down                  # Stop and remove the container
docker compose up -d --build         # Rebuild and restart (after code changes)
```

---

### Updating After Deployment

**To update documentation (no rebuild needed):**

1. Edit or add `.md` files in the `docs/` folder (mounted as a volume, so changes are reflected immediately)
2. In Discord, type `!ingest` (requires administrator permissions)
3. The bot reloads all docs immediately — no restart needed

**To update code:**

1. Pull or copy the updated files
2. Rebuild: `docker compose up -d --build`

---

## Cost Estimation

LLM pricing (pay-as-you-go):
- Input tokens: ~$3 per million tokens
- Output tokens: ~$15 per million tokens

Each user interaction costs roughly **$0.005–$0.01** depending on how many docs are retrieved and whether tool calls are made.

| Usage level | Monthly cost |
|-------------|-------------|
| ~10 queries/day (small group) | $2–5/month |
| ~50 queries/day (active community) | $10–20/month |
| ~100 queries/day (large server) | $20–35/month |

Set spending limits in your LLM provider's console to avoid surprises.

---

## Project Structure

```
apollo-bot/
├── bot.py                # Discord bot entry point
├── llm.py                # LLM API + tool definitions
├── rag.py                # ChromaDB ingestion & retrieval (RAG engine)
├── ingest.py             # Standalone script to load docs into ChromaDB
├── config.py             # Environment configuration
├── tools/
│   ├── __init__.py
│   ├── media_requests.py # Media request service API client
│   ├── movies.py         # Movie service API client
│   ├── shows.py          # TV show service API client
│   └── activity.py       # Activity monitoring API client
├── docs/                 # Markdown documentation (RAG knowledge base)
├── data/                 # ChromaDB persistent storage (auto-created)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Extending

**Add a new tool integration:**

1. Create a new file in `tools/` (e.g., `tools/transcoder.py`) — follow the pattern in `tools/movies.py`
2. Add the tool definition to the `TOOLS` list in `llm.py`
3. Add the handler to `TOOL_HANDLERS` dict in `llm.py`

**Add backend admin support:**

Create a second channel (e.g., `#apollo-admin`) and extend `bot.py` to detect messages there. Use a different system prompt in `llm.py` for admin messages that includes backend-focused instructions and unlocks tools like `get_system_status()`.
