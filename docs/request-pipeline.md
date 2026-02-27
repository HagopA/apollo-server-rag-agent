# How Your Request Works — The Full Pipeline

## Overview

This document explains the complete journey of a media request, from the moment you click "Request" to the moment it appears in your Plex library. Every step is fully automated — there are no manual steps by the server admin.

## Step 1: Cloudflare Tunnel — Access

Before you even reach the request page, your connection passes through a Cloudflare Tunnel. This keeps your access **secure and available from anywhere in the world** — no complicated setup needed on your end. The tunnel also acts as a security gate, ensuring only approved users can access the system.

## Step 2: The Media Request Service — Requests

The media request service is the request portal — this is where your journey starts. It's a clean, user-friendly web interface where you can search for any movie, TV show, or anime and hit "Request." Your request is **automatically approved** the moment you submit it and is immediately passed on to the right manager — no waiting required.

The current request service replaced a previous, now-deprecated version. The migration fixed TV show and anime ordering discrepancies between the request manager and the download services.

## Step 3: Routed by Content Type

Once approved, the request is routed based on what type of content it is:

- **Movie requests** go to the **movie management service**
- **TV show and anime requests** go to the **TV management service**

## Step 4: Movie Service / TV Service

**The movie service** takes charge of your movie requests. It tracks down the best quality release available and manages your entire movie library.

**The TV show service** manages all TV shows and anime. It monitors series and automatically picks up new episodes as they become available.

Both services work with quality profiles managed by the quality profile manager to ensure consistent quality standards:
- Movies are fetched in 4K (2160p) balanced quality
- TV shows and anime are fetched in 1080p balanced quality

## Step 5: Search Indexer — Searching for the Best Release

**The search indexer** is the search engine working behind the scenes. It queries multiple release sources on behalf of the movie and TV show services, finds what you requested, and sends the best match back to them. Think of it as a meta-search engine that checks many sources at once to find the best available version of what you want.

**The challenge solver** works alongside the search indexer. Some release sources are protected by anti-bot systems (like Cloudflare challenges). The challenge solver silently solves these challenges so the search indexer can access them without any interruptions. You'll never notice it working — it just quietly ensures the search process runs smoothly.

## Step 6: Download Client — Downloading

The download client receives the chosen release and handles retrieving it. Once the download is complete, it automatically notifies the movie or TV show service that the file is ready for the next step.

## Step 7: Tdarr — Processing

Before anything lands in your library, Tdarr automatically **cleans up every file** — stripping out unwanted audio tracks and subtitles so only the languages you need are kept. This happens according to the following rules:

**Movies:**
- English audio is always kept
- If the film's original language isn't English, both the original language audio and English audio are preserved
- English subtitles only

**TV Shows & Anime:**
- English audio only
- English subtitles only

This processing step is critical for saving storage space. Downloaded files often include many extra audio tracks (Italian, Spanish, German, etc.) that take up significant storage. Removing them keeps the server healthy and storage usage under control.

## Step 8: Plex — Streaming

Your content is now in Plex and **ready to watch**. Plex detects the new file, fetches artwork and all the metadata, and makes it available across all your devices. You'll receive a notification letting you know your request is ready to stream.

## Background Services — Always Running

In addition to the request pipeline, two services run continuously in the background:

**Quality Profile Manager:** Keeps quality standards consistent across the server. It automatically syncs quality profiles and custom formats with community-maintained databases, ensuring the system always grabs the best possible version of content. Movies are fetched in 4K (2160p) balanced quality, and TV shows and anime are fetched in 1080p balanced quality.

**Queue Cleanup Service:** Monitors the download queue and automatically removes any stalled or failed download attempts, keeping the system healthy and running smoothly without any manual intervention. If a download is blocked or stuck, the cleanup service removes it and can trigger a new search to find a replacement.

## Important Notes

- **All requests are automatically approved** — you don't need to wait for admin approval
- **The entire process is fully automated** — from request to available on Plex, no human intervention is needed
- **Typical wait time is 15 minutes to a few hours** depending on file size and availability
- If something seems stuck or isn't appearing, check with the Apollo Bot for a status update
