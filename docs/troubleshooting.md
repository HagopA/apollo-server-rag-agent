# Troubleshooting Guide

## Request Issues

### My request is stuck in "Processing" for a long time

This usually means the system is still searching for or downloading the content. A few things could be happening:

- **The release isn't available yet** — If the content is very new (just released in theaters, or a brand new episode), it may take time for a good quality release to appear online. The system will keep searching automatically.
- **Large file size** — A 4K movie can be 40-80GB, which takes time to download depending on available bandwidth.
- **Slow or limited sources** — Sometimes the available sources have slow speeds. The system will complete the download, it just takes longer.
- **The download is stalled** — Occasionally a download can stall with no connections. Cleanuparr monitors for this and will automatically remove stalled downloads and trigger a new search. This can cause a brief delay but is self-correcting.

**What to do:** Wait a few hours. If it's still stuck after 24 hours, let the admin know.

### My request was approved but nothing is downloading

The system may still be searching for an available release. This is common for:
- Brand new content that just came out
- Older or obscure titles with limited availability
- Content that hasn't been officially released yet

The system continues to search automatically. Once a qualifying release appears, the download will start.

### I see "Available" in Seerr but it's not in Plex

There can be a short delay between Tdarr finishing the file processing and Plex picking up the new file. Try:

1. Wait 5-10 minutes — Plex scans for new content periodically
2. Pull down to refresh your library in the Plex app
3. Search for the title directly using the Plex search bar
4. Check the correct library — movies are in the Movies library, TV shows in TV Shows, and anime in the Anime library

## Playback Issues

### Video is buffering or stuttering

Buffering is usually caused by one of the following:

**Your internet connection:** Streaming high-quality content requires a stable connection. 4K content needs approximately 25-40 Mbps, and 1080p needs approximately 8-15 Mbps.

**Plex quality settings:** If your Plex app is set to a lower quality than the source file, the server has to transcode (re-encode) the video in real-time, which can cause buffering. Set your quality to "Maximum" or "Original" in Plex settings to avoid this.

**Remote streaming:** If you're streaming from outside your home, your connection goes through the Cloudflare Tunnel. While this works well in most cases, very high-bandwidth 4K streams may occasionally buffer on slower connections.

**WiFi vs. Ethernet:** If you're on WiFi and experiencing buffering, try connecting your device via Ethernet for a more stable connection.

### Video quality looks poor

Check your Plex streaming quality settings:
- **Plex Web:** Click your profile icon → Settings → Quality → set to Maximum or Original
- **Plex Mobile:** Settings → Quality → adjust both "Remote Streaming" and "Home Streaming" to Maximum
- **Plex TV App:** Settings → Video Quality → set to Maximum or Original

If you're on mobile data, Plex may automatically lower quality to save data. You can override this in the mobile app settings.

### Audio is missing or in the wrong language

All content is processed to keep English audio only (with original language audio preserved for non-English movies). If you're expecting audio in a different language:

- **For movies:** Check if the movie's original language is English. If so, only English audio is kept. If the movie is originally in another language (e.g., Korean, Japanese), both the original audio and English should be available.
- **For TV shows and anime:** Only English audio is kept. If you need the original language audio, contact the admin.
- **Subtitle settings:** Make sure subtitles are enabled in your Plex player if needed. English subtitles should be available on all content.

### Content is playing but subtitles are missing

Subtitles may need to be manually enabled in your Plex player:
1. While playing, look for the speech bubble or subtitle icon
2. Select "English" from the available subtitle tracks
3. If no subtitles appear, the file may not have embedded subtitles — contact the admin

## Access Issues

### I can't access the request portal

- Make sure you're going to the correct URL: **https://requests.apollohub.ca/**
- Check that you're signing in with the correct Google account (the one associated with your Plex email)
- Try clearing your browser cache and cookies, then try again
- If you've never accessed the portal before, the admin may need to add your Google email to the approved list

### Plex says "Not Authorized" or "Server Unavailable"

- Make sure you're signed in to the correct Plex account
- Check that the Plex app is up to date
- The server may be temporarily down for maintenance — wait a few minutes and try again
- If the issue persists, contact the admin

### The request portal loads but Seerr shows an error

- Try refreshing the page
- Clear your browser cache and try again
- If you see a TMDB-related error, this is usually temporary and resolves on its own

## General Issues

### How do I know if the server is down?

If you can't reach Plex or the request portal, the server may be undergoing maintenance or an update. Check the Discord announcements channel for any notices. You can also ask the Apollo Bot for a status check.

### Something else is wrong

If none of the above covers your issue, reach out in the Discord support channel or message the admin directly. Include:
- What you were trying to do
- What happened (or didn't happen)
- The title of the content if applicable
- What device you're using
