# Frequently Asked Questions

## Requesting Content

### How do I request a movie, TV show, or anime?

Go to the request portal at https://requests.apollohub.ca/, sign in through the Cloudflare security gate using your Google account, then sign in to Seerr with your Plex account. Search for what you want and click "Request." Your request is automatically approved — no waiting needed.

### Is there a limit on how many requests I can make?

There is no strict limit on the number of requests. Please be reasonable with your requests — the system is shared by multiple users and storage is finite.

### Can I request anime?

Yes. Anime is fully supported. Search for it in Seerr the same way you would a TV show. The system automatically routes anime to the correct manager (Sonarr) and places it in the dedicated Anime library in Plex.

### Can I request 4K content?

Movies are automatically fetched in 4K (2160p) balanced quality when available. TV shows and anime are fetched in 1080p quality. You don't need to do anything special — the system always grabs the best available quality based on these profiles.

### What happened to Overseerr?

Overseerr has been deprecated and replaced by Seerr. Seerr is a unified successor that combines Overseerr and Jellyseerr into a single project. The migration fixed TV show and anime ordering discrepancies that existed with Overseerr. The request portal URL remains the same: https://requests.apollohub.ca/

### Can I use my Plex Watchlist to make requests?

Seerr supports Plex Watchlist auto-request. If this feature is enabled, simply adding content to your Plex Watchlist will automatically create a request in Seerr.

## After Requesting

### I requested something but it's not showing up on Plex yet

Don't worry — the process takes time. Here's what to check:

1. **Check Seerr** — Is your request still showing as "Processing"? That means it's still being downloaded or processed
2. **Wait 15-30 minutes** — Most content appears within this timeframe after the status changes to "Available"
3. **Refresh your Plex app** — Sometimes Plex needs a moment to scan new files. Pull down to refresh or restart the app
4. **Ask the Apollo Bot** — Type something like "check the status of [title]" and the bot will look it up for you

### How long does it take for my request to be available?

Typically **15 minutes to a few hours** after requesting. It depends on:
- **File size** — A 40GB 4K movie takes longer to download than a 2GB TV episode
- **Availability** — If the release just came out, it may take time for good quality versions to appear
- **Processing time** — Tdarr needs to clean up the file after download, which adds a few minutes

### My request says "Available" but I can't find it in Plex

Try these steps:
1. Search for the title directly in the Plex app search bar
2. Check if it's in the correct library (Movies, TV Shows, or Anime)
3. Pull down to refresh the library
4. Wait a few minutes — Plex scans for new content periodically, so there can be a short delay between the file being added and Plex picking it up

### Why was my request declined?

Requests are rarely declined since they are automatically approved. If yours shows as declined, it may be because:
- The title is not yet released
- There was a technical issue — reach out to the admin
- The title was already available in Plex (check your library)

### Can I cancel a request?

You can cancel pending requests through Seerr. Go to your request page and look for the cancel option. Once a download has started, contact the admin if you need it removed.

## Plex & Streaming

### What devices can I use to watch?

Plex works on virtually everything: smart TVs (Samsung, LG, Sony, etc.), phones and tablets (iOS and Android), computers (web browser or desktop app), game consoles (PlayStation, Xbox), and streaming devices (Roku, Apple TV, Fire TV, Chromecast, NVIDIA Shield).

### Can I watch from outside my home?

Yes. The server is accessible from anywhere in the world through a Cloudflare Tunnel. Just open your Plex app and sign in — it works the same whether you're at home or traveling.

### Something is playing in bad quality or buffering

If you're experiencing buffering or low quality:
1. **Check your internet connection** — streaming requires a stable connection, especially for high-quality content
2. **Check your Plex quality settings** — make sure they're set to "Maximum" or "Original" rather than a lower quality. Go to Settings → Quality in the Plex app
3. **Mobile data** — if you're on cellular data, Plex may automatically lower quality to save data. Adjust this in the Plex mobile app settings
4. **Try a different device** — if one device buffers, try another to rule out device-specific issues

### Why is the audio only in English?

To save storage space, the server keeps only English audio and subtitles for TV shows and anime. For movies, the original language audio is preserved alongside English if the film isn't originally in English. If you need a specific show or anime in its original language, let the admin know and they can grab that version manually.

### Where is the Anime library?

Anime has its own dedicated library in Plex, separate from TV shows. This is because anime handles seasons, episode numbering, and specials differently than regular TV. Look for the "Anime" library in your Plex sidebar. You can pin it for quick access.

## Account & Access

### How do I sign in to the request portal?

Access involves two steps:
1. **Cloudflare Security Gate** — Click "Sign in with Google" and use the Google account associated with your Plex email
2. **Seerr Login** — Click "Sign in with Plex" and complete the Plex sign-in

### Why are there two sign-in steps?

**Step 1 (Google)** confirms you're an approved member of the server using your trusted Google account. This is a security gate because the server's local network is exposed to the internet, and this step ensures only authorized users can access it.

**Step 2 (Plex)** links your session to your Plex profile so Seerr knows which requests belong to you.

### I'm having trouble signing in

Make sure you're using the same Google account email that's associated with your Plex account. If you're still having issues, contact the admin.

## How Things Work Behind the Scenes

### What is Seerr?

Seerr is the request management portal. It's a web interface where you search for movies, TV shows, and anime and submit requests. It integrates with Plex to show what's already available, and with Radarr and Sonarr to process new requests.

### What are Radarr and Sonarr?

Radarr manages movies and Sonarr manages TV shows and anime. When you make a request in Seerr, it gets passed to the appropriate manager, which then handles finding, downloading, and organizing the content.

### How does the server know what quality to download?

Quality profiles are managed by Profilarr, which automatically syncs with community-maintained quality databases. This ensures the server always grabs the best possible version based on the defined profiles (4K for movies, 1080p for TV/anime).

### What's new on the server?

Check the "Recently Added" section on your Plex home screen, or ask the Apollo Bot — it can tell you what's been recently added.
