# Apollo Media Server — User Guide

## Welcome to Apollo

Apollo is your private media server powered by Plex. It gives you access to a growing library of movies, TV shows, and anime — all available to stream on any device, anywhere in the world. New content is added through a fully automated request system, so you can request what you want and it will be downloaded, processed, and added to Plex for you.

## How to Access the Request Portal

The request portal is hosted at **https://requests.apollohub.ca/**. Accessing it involves two quick sign-in steps:

**Step 1 — Security Gate (Cloudflare Access via Google):** When you first open the link, you'll see a Cloudflare security login screen. Click "Sign in with Google" and select the Google account that's associated with your Plex email. This verifies you're an approved member of the server.

**Step 2 — Seerr Login (via Plex):** After passing the security gate, you'll land on the Seerr login page. Click "Sign in with Plex" and complete the Plex sign-in if prompted. This links your session to your Plex profile so the system knows which requests belong to you.

After both steps, you'll be taken directly into the Seerr request portal where you can search for and request content.

## How to Request Content

1. Open the request portal at **https://requests.apollohub.ca/**
2. Sign in using the two-step process described above
3. Use the search bar to find any movie, TV show, or anime
4. Click on the title you want
5. Click the **Request** button
6. Your request is **automatically approved** the moment you submit it — no waiting for manual approval

That's it. The system takes over from here and handles everything automatically.

## What Happens After You Submit a Request

Once your request is submitted, the following happens entirely automatically behind the scenes:

1. **Request submitted in Seerr** — Your request is instantly approved and passed to the right download manager based on content type
2. **Routed by content type** — Movie requests go to Radarr (the movie manager). TV show and anime requests go to Sonarr (the TV/anime manager)
3. **Best release searched** — Prowlarr, the search engine, queries multiple release sources to find the best quality version available. Some sources are protected by anti-bot systems, and Byparr silently handles those challenges so the search runs smoothly
4. **Download begins** — The best matching release is sent to the download manager (qBittorrent), which retrieves the file
5. **File is processed by Tdarr** — Before anything lands in your library, Tdarr automatically cleans up the file by removing unnecessary audio tracks and subtitles (see the Audio & Subtitle Policy section below)
6. **Added to Plex** — The processed file is added to your Plex library. Plex detects it, fetches artwork and metadata, and makes it available across all your devices. You'll receive a notification letting you know your request is ready to stream

This entire process typically takes anywhere from **15 minutes to a few hours**, depending on availability and file size.

## Audio and Subtitle Policy

To save storage space and keep things consistent, all downloaded content is automatically processed with the following rules:

**Movies:**
- English audio is always kept
- If the film's original language is not English, both the original language audio and English audio are preserved
- English subtitles only

**TV Shows:**
- English audio only
- English subtitles only

**Anime:**
- English audio only
- English subtitles only

These rules are applied automatically by Tdarr after every download. This means extra audio tracks (Italian, Spanish, German, etc.) and unnecessary subtitle tracks are removed to save significant storage space.

If you ever want a specific show or anime in its original language, just let the server admin know — they can grab that version manually for you.

## Quality Profiles

All content is downloaded in the best available quality thanks to Profilarr, which keeps quality standards consistent across the server:

- **Movies** are fetched in **4K (2160p) balanced quality** when available, with fallback to lower resolutions
- **TV Shows and Anime** are fetched in **1080p balanced quality**

The system automatically upgrades to better quality versions as they become available.

## Anime

Anime has its own dedicated library in Plex, separate from regular TV shows. This was done because anime is handled very differently than standard TV shows — things like seasons, episode numbering, specials, and artwork don't always follow the same rules. Keeping anime separate lets Plex handle it properly, resulting in cleaner organization, more accurate metadata, and fewer edge cases.

You don't need to do anything differently to request anime. Just search for it in Seerr the same way you would a TV show, and the system routes it to the right place automatically. If you want quick access, pin the Anime library in your Plex app.

## Plex — Watching Your Content

Once content is available, you watch it through the **Plex** app. Plex works on smart TVs, phones, tablets, computers, game consoles, and streaming devices like Roku, Apple TV, Fire TV, and Chromecast. Download the Plex app on your device and sign in with your Plex account.

Your content is available from anywhere in the world thanks to the Cloudflare Tunnel, which provides a secure connection to the server without any complicated setup on your end.

## Need Help?

If you have any questions or run into issues, you can ask here in the Discord support channel. The Apollo Bot can help you with:

- Checking the status of your requests
- Showing what's currently downloading
- Telling you what's been recently added to the library
- Explaining how the system works
- Troubleshooting common issues

Just type your question and the bot will do its best to help!
