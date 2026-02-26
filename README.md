# 🚀 Apollo Bot

A RAG-powered AI support chatbot for your private Plex media server, built with Claude and Discord.

Apollo Bot answers user questions using your documentation, and can check real-time data from Seerr, Radarr, Sonarr, and Tautulli via Claude's tool use.

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
    ↓
bot.py (Discord listener + thread management)
    ↓
llm.py (Claude API + tool orchestration)
    ├── rag.py → ChromaDB (document retrieval)
    └── tools/ → Seerr / Radarr / Sonarr / Tautulli APIs
    ↓
Response → Discord
```

---

## Setup Guide

### Prerequisites

You'll need the following before starting:

- **Python 3.11 or 3.12** — Download from https://www.python.org/downloads/. During installation, **check "Add Python to PATH"** — this is critical.
- **PyCharm** — You already have this. The Community Edition works fine.
- **Git** (optional but recommended) — https://git-scm.com/download/win
- **Docker Desktop** (for local testing) — https://www.docker.com/products/docker-desktop/ — OR you can skip this and deploy directly to Unraid.

To verify Python is installed, open a terminal (PowerShell or Command Prompt) and run:

```
python --version
```

You should see something like `Python 3.12.x`.

---

### Step 1. Create a Discord Bot

This gives you the bot account that will live in your Discord server.

1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it "Apollo Assistant" → click **Create**
3. In the left sidebar, click **Bot**
4. Click **Reset Token** → confirm → **copy the token immediately** (you won't see it again). Save it somewhere safe — this goes in your `.env` file later as `DISCORD_BOT_TOKEN`.
5. Scroll down to **Privileged Gateway Intents** and enable:
   - ✅ **Message Content Intent** (required for the bot to read messages)
6. In the left sidebar, click **OAuth2** → **URL Generator**
7. Under **Scopes**, check: `bot`
8. Under **Bot Permissions**, check:
   - `Send Messages`
   - `Create Public Threads`
   - `Send Messages in Threads`
   - `Read Message History`
9. Copy the **Generated URL** at the bottom of the page
10. Paste the URL into your browser → select your Discord server → **Authorize**

The bot now appears in your server (offline — it will come online when you run the code).

**One more thing:** Create a channel in your Discord server for the bot (e.g., `#ask-apollo`). Right-click the channel → **Copy Channel ID**. (If you don't see this option, go to Discord Settings → Advanced → enable **Developer Mode**.) Save this ID — it goes in your `.env` as `DISCORD_CHANNEL_ID`.

---

### Step 2. Get Your API Keys

You need API keys from each service. Here's exactly where to find them:

| Service      | How to get the key |
|--------------|-------------------|
| **Anthropic** | Go to https://console.anthropic.com/settings/keys → Create a new key. You'll need to add credit ($5 minimum). This is a pay-as-you-go API — see cost estimate below. |
| **Seerr**     | Open Seerr web UI → **Settings** → **General** → scroll to **API Key** → copy it |
| **Radarr**    | Open Radarr web UI → **Settings** → **General** → **Security** section → **API Key** |
| **Sonarr**    | Open Sonarr web UI → **Settings** → **General** → **Security** section → **API Key** |
| **Tautulli**  | Open Tautulli web UI → **Settings** → **Web Interface** → **API Key** |

Keep all of these handy — you'll paste them into the `.env` file in Step 4.

---

### Step 3. Open the Project in PyCharm

1. Download/extract the `apollo-bot` folder to somewhere on your Windows machine (e.g., `C:\Projects\apollo-bot`)
2. Open **PyCharm** → **File** → **Open** → select the `apollo-bot` folder
3. PyCharm will open the project. You should see all the files in the left sidebar.

**Set up a Python interpreter (virtual environment):**

This is the Python equivalent of a Java SDK/JDK setup. A virtual environment isolates this project's dependencies (like a Maven `pom.xml` scope).

4. Go to **File** → **Settings** (or `Ctrl+Alt+S`)
5. Navigate to **Project: apollo-bot** → **Python Interpreter**
6. Click the gear icon ⚙️ → **Add Interpreter** → **Add Local Interpreter**
7. Select **Virtualenv Environment** → **New**
   - Location: leave the default (it'll be inside your project folder)
   - Base interpreter: select your Python 3.11 or 3.12 installation
8. Click **OK** → **OK**

PyCharm will create a `.venv` folder in your project. This is like a project-local Maven `.m2` — it holds all your dependencies.

**Install dependencies:**

9. Open the **Terminal** tab at the bottom of PyCharm (it automatically activates your virtual environment — you'll see `(.venv)` at the start of the prompt)
10. Run:

```
pip install -r requirements.txt
```

This is the Python equivalent of `mvn install`. It reads `requirements.txt` (like `pom.xml`) and downloads all dependencies. You'll see packages installing — this takes a minute or two.

---

### Step 4. Configure Your Environment Variables

The `.env` file is how Python projects handle configuration (similar to `application.properties` in Spring Boot).

1. In PyCharm's file explorer, find `.env.example`
2. Right-click it → **Copy** → right-click the project root → **Paste** → rename the copy to `.env`
3. Open `.env` and fill in your values:

```env
# --- Discord ---
DISCORD_BOT_TOKEN=paste_your_discord_bot_token_here
DISCORD_CHANNEL_ID=paste_your_channel_id_here

# --- Anthropic (Claude) ---
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# --- Seerr ---
SEERR_URL=http://apollo.local:5055
SEERR_API_KEY=paste_seerr_key_here

# --- Radarr ---
RADARR_URL=http://apollo.local:7878
RADARR_API_KEY=paste_radarr_key_here

# --- Sonarr ---
SONARR_URL=http://apollo.local:8989
SONARR_API_KEY=paste_sonarr_key_here

# --- Tautulli ---
TAUTULLI_URL=http://apollo.local:8181
TAUTULLI_API_KEY=paste_tautulli_key_here
```

**Important notes on the URLs:**
- Replace `apollo.local` with however you access your Unraid services. This could be `apollo.local`, `192.168.x.x`, or a domain name.
- The port numbers should match what your containers are actually using. The ones above are defaults — check your Unraid Docker tab if unsure.
- When running from your Windows machine (for development/testing), your PC must be able to reach these URLs. Test by opening one in your browser (e.g., `http://apollo.local:5055`).

---

### Step 5. Add Your Documentation

The `docs/` folder is the bot's knowledge base. Every `.md` (Markdown) file in this folder gets chunked and embedded into a vector database so the bot can search through it when answering questions.

A sample `docs/user-guide.md` is included. You should **expand it and add more files** based on your actual Apollo setup. Here's what to include:

**Recommended doc files to create:**

| File | What to put in it |
|------|------------------|
| `docs/user-guide.md` | Already included. Edit it to match your actual setup, quality profiles, and policies. |
| `docs/requesting.md` | Detailed walkthrough of how to use Seerr — step by step with screenshot descriptions. Paste your existing flowchart descriptions here. |
| `docs/troubleshooting.md` | Common problems and solutions: "media not appearing," "buffering issues," "request stuck in processing," etc. |
| `docs/faq.md` | Answers to questions your users actually ask you repeatedly. |
| `docs/server-rules.md` | Any rules or policies (request limits, content policies, etc.) |
| `docs/anime.md` | Anime-specific info if your users request a lot of anime (dual audio, subgroups, etc.) |

**Tips for writing good docs:**
- Write them as if you're explaining to a user, not as technical notes.
- Use `## Headings` to organize sections — the RAG chunker splits on these headings, so each section becomes a retrievable chunk.
- Be specific. "Movies download in up to 4K HDR" is better than "we get good quality."
- The more docs you add, the smarter the bot gets. You can always add more later and run `!ingest` to reload.

---

### Step 6. Test Locally (On Your Windows Machine)

Before deploying to Unraid, test that everything works from your PC.

**6a. Ingest your documentation:**

In PyCharm's terminal:

```
python ingest.py
```

You should see output like:

```
📥 Ingesting documentation from ./docs/

  ✅ user-guide.md: 8 chunks

📚 Ingested 8 chunks from 1 files.

✅ Ready! You can test with: python ingest.py query 'how do I request a movie'
```

**6b. Test that retrieval works:**

```
python ingest.py query "how do I request a movie"
```

This searches your docs and shows the most relevant chunks. If you get results, RAG is working.

**6c. Run the bot:**

```
python bot.py
```

You should see:

```
🚀 Starting Apollo Assistant...
INFO     apollo-bot: ✅ Apollo Assistant is online as ApolloAssistant#1234
INFO     apollo-bot:    Listening in channel ID: 123456789
```

**6d. Test in Discord:**

Go to your `#ask-apollo` channel and type:
- `!status` — Should reply confirming the bot is online
- `How do I request a movie?` — Should create a thread and answer from your docs
- `What's currently downloading?` — Should call the Radarr/Sonarr APIs and report real status
- `Check the status of Oppenheimer` — Should search Seerr for that title

**If something goes wrong:**
- **"DISCORD_BOT_TOKEN is not set"** → Your `.env` file isn't being found. Make sure it's named exactly `.env` (not `.env.txt`) and is in the project root folder (same level as `bot.py`).
- **Connection errors to Seerr/Radarr** → Your Windows PC can't reach the Unraid services. Check the URLs in `.env` and test them in your browser.
- **Anthropic API errors** → Check that your API key is correct and that you've added credit to your Anthropic account.
- **"ModuleNotFoundError"** → Dependencies aren't installed. Make sure your PyCharm terminal shows `(.venv)` at the start and re-run `pip install -r requirements.txt`.

Press `Ctrl+C` in the terminal to stop the bot.

---

### Step 7. Deploy to Unraid

Once everything works locally, deploy to Unraid so the bot runs 24/7.

**7a. Copy the project to Unraid:**

Copy the entire `apollo-bot` folder to your Unraid server. A common location:

```
/mnt/user/appdata/apollo-bot/
```

You can use Windows File Explorer if you have a network share set up to your Unraid server (`\\TOWER\appdata\` or similar), or use SCP/SFTP.

**Make sure to include:**
- All `.py` files and the `tools/` folder
- Your `.env` file (with real values filled in)
- The `docs/` folder with your documentation
- `Dockerfile`, `docker-compose.yml`, `requirements.txt`

**Do NOT copy** the `.venv` folder or the `data/` folder — the virtual environment is Windows-specific and won't work on Linux, and the data folder will be recreated inside the container.

**7b. Update `.env` URLs for Unraid:**

When running on Unraid itself, your service URLs change. Since the `docker-compose.yml` uses `network_mode: host`, the bot container shares Unraid's network stack. You can use:

- `http://localhost:PORT` — simplest option with host networking
- `http://192.168.x.x:PORT` — your Unraid's LAN IP (always works)

Open the `.env` on Unraid and update the URLs:

```env
SEERR_URL=http://localhost:5055
RADARR_URL=http://localhost:7878
SONARR_URL=http://localhost:8989
TAUTULLI_URL=http://localhost:8181
```

**7c. Build and start the container:**

SSH into your Unraid server (or use the terminal from the Unraid web UI) and run:

```bash
cd /mnt/user/appdata/apollo-bot
docker compose up -d --build
```

Breaking this down:
- `docker compose up` — starts the services defined in `docker-compose.yml`
- `-d` — runs in the background (detached mode), like `nohup` or a systemd service
- `--build` — builds the Docker image from the Dockerfile first

First run takes a few minutes as it downloads the Python base image and installs dependencies. Subsequent rebuilds are much faster thanks to Docker layer caching.

**7d. Check that it's running:**

```bash
docker logs apollo-bot
```

You should see the same startup messages as when you ran locally. The bot should show as online in Discord.

**7e. Useful Docker commands for ongoing management:**

```bash
docker logs apollo-bot --tail 50     # View last 50 log lines
docker logs apollo-bot -f            # Follow logs in real-time (Ctrl+C to exit)
docker compose restart               # Restart the bot
docker compose down                  # Stop and remove the container
docker compose up -d --build         # Rebuild and restart (after code changes)
```

---

### Step 8. Updating After Deployment

**To update documentation (no rebuild needed):**

1. Edit or add `.md` files in the `docs/` folder on Unraid (the folder is mounted as a volume, so changes are reflected immediately)
2. In Discord, type `!ingest` (you must have administrator permissions in the Discord server)
3. The bot reloads all docs immediately — no restart needed

**To update code:**

1. Make changes in PyCharm on your Windows machine
2. Test locally with `python bot.py`
3. Copy the changed files to Unraid's `/mnt/user/appdata/apollo-bot/`
4. Rebuild: `cd /mnt/user/appdata/apollo-bot && docker compose up -d --build`

---

## Cost Estimation

Claude Sonnet pricing (pay-as-you-go):
- Input tokens: ~$3 per million tokens
- Output tokens: ~$15 per million tokens

For this bot, each user interaction costs roughly **$0.005–$0.01** depending on how many docs are retrieved and whether tool calls are made. Realistic usage:

| Usage level | Monthly cost |
|-------------|-------------|
| ~10 queries/day (small friend group) | $2–5/month |
| ~50 queries/day (active community) | $10–20/month |
| ~100 queries/day (large server) | $20–35/month |

You can set spending limits in the Anthropic Console at https://console.anthropic.com to avoid surprises.

---

## Project Structure

```
apollo-bot/
├── bot.py              # Discord bot entry point (like your Main class)
├── llm.py              # Claude API + tool definitions (like a service layer)
├── rag.py              # ChromaDB ingestion & retrieval (the RAG engine)
├── ingest.py           # Standalone script to load docs into ChromaDB
├── config.py           # Environment configuration (like application.properties)
├── tools/
│   ├── __init__.py     # Package marker (like a package-info.java)
│   ├── seerr.py        # Seerr API client
│   ├── radarr.py       # Radarr API client
│   ├── sonarr.py       # Sonarr API client
│   └── tautulli.py     # Tautulli API client
├── docs/               # Your markdown documentation (RAG knowledge base)
│   └── user-guide.md   # Sample user guide
├── data/               # ChromaDB persistent storage (auto-created)
├── Dockerfile          # Container build instructions
├── docker-compose.yml  # Container orchestration config
├── requirements.txt    # Dependencies (like pom.xml)
└── .env.example        # Template for environment variables
```

**Java developer mental model:**
- `bot.py` = your `@SpringBootApplication` main class with event listeners
- `llm.py` = a `@Service` that orchestrates AI calls and tool execution
- `rag.py` = a `@Repository` that handles vector DB operations
- `tools/*.py` = `@Component` REST clients (like using `RestTemplate` / `WebClient`)
- `config.py` = `@Configuration` + `@Value` annotations
- `requirements.txt` = `pom.xml` dependencies
- `.env` = `application.properties`

---

## Extending

**Add a new tool integration:**

1. Create a new file in `tools/` (e.g., `tools/tdarr.py`) — follow the pattern in `tools/radarr.py`
2. Add the tool definition to the `TOOLS` list in `llm.py` (this tells Claude the tool exists)
3. Add the handler to `TOOL_HANDLERS` dict in `llm.py` (this maps the tool name to your function)

**Add backend admin support:**

Create a second channel (e.g., `#apollo-admin`) and extend `bot.py` to detect messages there. Use a different system prompt in `llm.py` for admin messages that includes backend-focused instructions and unlocks tools like `get_system_status()`.
