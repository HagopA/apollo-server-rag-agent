# Apollo Services Overview

## What Each Service Does

Apollo runs on a suite of specialized services, each handling a specific part of the media pipeline. Here's what each one does and how they work together.

## User-Facing Services

### Seerr (Request Portal)

Seerr is the request management portal — the main interface you interact with. It's a web app where you search for movies, TV shows, and anime, and submit requests. Seerr integrates with Plex to show what's already available in the library, so you don't accidentally request something that already exists. It also integrates with Radarr and Sonarr to automatically pass approved requests to the right download manager.

Seerr replaced the previous request manager, Overseerr, which was deprecated. Seerr is the unified successor that combines the best of Overseerr and Jellyseerr into a single project, with improvements like better metadata handling and TVDB support.

URL: https://requests.apollohub.ca/

### Plex (Media Server / Streaming)

Plex is the media server — it's how you watch everything. Plex organizes your content into libraries (Movies, TV Shows, Anime), fetches artwork and metadata, and streams to your devices. It works on smart TVs, phones, tablets, computers, game consoles, and streaming devices.

The server has three main Plex libraries:
- **Movies** — All movie content
- **TV Shows** — Standard television series
- **Anime** — All anime content (separate from TV shows for better organization and metadata accuracy)

## Download Management

### Radarr (Movie Manager)

Radarr is a movie collection manager. When you request a movie through Seerr, Radarr receives the request, searches for the best quality version available, sends it to the download client, and then renames and organizes the file once downloaded. Radarr monitors for quality upgrades — if a better version of a movie becomes available later, it can automatically upgrade.

### Sonarr (TV & Anime Manager)

Sonarr does the same thing as Radarr, but for TV shows and anime. It manages series, monitors for new episodes as they air, and automatically downloads them. Sonarr tracks which episodes you have and which you're missing, and fills in gaps automatically.

### Prowlarr (Search Indexer)

Prowlarr is the centralized search engine for the entire system. Rather than Radarr and Sonarr each having their own search configurations, Prowlarr manages all indexers (search sources) in one place and syncs them to both Radarr and Sonarr. When either app needs to find a release, the search goes through Prowlarr, which queries multiple sources simultaneously and returns the best matches.

### Byparr (Anti-Bot Bypass)

Some release sources protect themselves with anti-bot challenges (like Cloudflare's browser verification). Byparr works alongside Prowlarr to silently solve these challenges, ensuring that Prowlarr can access all configured sources without interruption. Users never interact with Byparr — it works entirely in the background.

### qBittorrent (Download Client)

qBittorrent is the download client — it's the application that actually downloads the files. When Radarr or Sonarr find a release they want, they send a download request to qBittorrent, which handles retrieving the file. Once the download is complete, the file is handed back to Radarr or Sonarr for import and organization.

## Processing & Quality

### Tdarr (Media Processing)

Tdarr is a media processing application that automatically cleans up every file before it reaches your Plex library. It removes unnecessary audio tracks and subtitles based on configured rules:

- **Movies:** Keeps English audio (plus original language if non-English). English subtitles only.
- **TV Shows:** English audio and English subtitles only.
- **Anime:** English audio and English subtitles only.

Tdarr uses FFmpeg and HandBrake under the hood to process files. This step is important because downloaded files often include many extra audio tracks and subtitles in languages that aren't needed, and those extra tracks consume significant storage space.

### Profilarr (Quality Profile Management)

Profilarr manages quality profiles and custom formats for Radarr and Sonarr. It automatically syncs with community-maintained quality databases (like Dictionarry) to ensure the system always grabs the best possible version of content based on defined standards:

- **Movies:** 4K (2160p) balanced quality
- **TV Shows and Anime:** 1080p balanced quality

Profilarr eliminates the need to manually configure quality rules — it handles everything automatically and keeps the profiles up to date as media standards evolve.

### Cleanuparr (Queue Cleanup)

Cleanuparr monitors the download queues in Radarr and Sonarr and automatically cleans up any problems. If a download is stalled, blocked, contains malicious files, or has failed, Cleanuparr removes it and can trigger a new search to find a replacement. Think of it as the server's janitor — it keeps the download queue clean and running smoothly without any manual intervention.

## Infrastructure

### Cloudflare Tunnel (Secure Remote Access)

The Cloudflare Tunnel provides secure access to the server from anywhere in the world. Instead of exposing the server directly to the internet, all connections are routed through Cloudflare's network, which provides encryption and protection. This is why both Plex and the request portal work seamlessly whether you're at home or traveling.

The tunnel also includes Cloudflare Access, which is the security gate (Google sign-in) that you encounter when accessing the request portal. This ensures only approved users can reach the system.

### Tautulli (Monitoring)

Tautulli is a monitoring and statistics tool for Plex. It tracks what's being streamed, who's watching, and provides detailed playback statistics. The admin uses Tautulli to monitor server health and streaming activity.

### Uptime Kuma (Uptime Monitoring)

Uptime Kuma monitors the availability of all services. If any service goes down, it sends alerts so the admin can address the issue quickly.
