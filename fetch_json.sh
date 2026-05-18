#!/bin/bash
# 从 GitHub raw 拉取最新的 beeweb_today.json
# jsDelivr 备选 (CDN缓存12小时, 适合GitHub被墙时用)
RAW_URL="https://raw.githubusercontent.com/tbx723623/anime-scraper/main/beeweb_today.json"
CDN_URL="https://cdn.jsdelivr.net/gh/tbx723623/anime-scraper@main/beeweb_today.json"
DEST="/opt/anime-bot/beeweb_today.json"

# 先试 GitHub raw
if curl -fsSL --connect-timeout 15 -o "$DEST" "$RAW_URL"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fetched from GitHub raw"
    exit 0
fi

# 备用 jsDelivr CDN
if curl -fsSL --connect-timeout 15 -o "$DEST" "$CDN_URL"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fetched from jsDelivr CDN"
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Failed to fetch beeweb_today.json"
exit 1
