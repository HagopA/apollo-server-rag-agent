# Anime on Apollo

## Dedicated Anime Library

Anime has its own dedicated library in Plex, separate from regular TV shows. This separation was made because anime is handled very differently than standard television:

- **Season numbering** — Anime often uses absolute episode numbering rather than standard season/episode format. Some anime series have hundreds of episodes across unconventional season structures
- **Specials and OVAs** — Anime frequently includes specials, OVAs (Original Video Animations), and movies that don't fit neatly into a standard TV show structure
- **Artwork and metadata** — Anime-specific artwork, character info, and descriptions work better when Plex knows the content is anime

By keeping anime separate, Plex handles all of these things correctly, resulting in cleaner organization, more accurate metadata, and fewer weird edge cases. Nothing changes for you — just look for the **Anime** library in your Plex sidebar and pin it for quick access.

## How to Request Anime

Request anime the same way you request any other content:

1. Go to the request portal at https://requests.apollohub.ca/
2. Search for the anime title
3. Click **Request**

The system automatically recognizes anime and routes it to the TV management service (which manages both TV shows and anime), which then uses anime-specific quality profiles and file handling.

## Audio and Subtitles for Anime

Anime downloads follow these rules:

- **English audio only** (dubbed version when available)
- **English subtitles only**

This means the system grabs the English-dubbed version when one exists. If you specifically want the Japanese audio with subtitles for a particular anime, let the admin know — they can grab that version manually.

## Quality

Anime is fetched in **1080p balanced quality**, the same as regular TV shows. The quality profiles are maintained by the quality profile manager to ensure the best available version is always selected.

## Common Anime Questions

### Why is my anime showing wrong episode numbers?

The dedicated anime library should handle episode numbering correctly. If you notice incorrect numbering, it may be a metadata issue. Let the admin know and they can investigate.

### Can I request anime movies?

Yes. Anime movies are handled like regular movies — they'll be fetched in 4K quality when available and appear in the Movies library (not the Anime library, since they're films rather than series).

### Some anime episodes are missing

The TV show service monitors anime series for new episodes automatically. If episodes are missing, it could be because:
- The episodes haven't been released yet
- A good quality release hasn't been found yet — the system will keep searching
- There was a download issue — the queue cleanup service may be handling it automatically

If episodes remain missing after a day or two, contact the admin.
