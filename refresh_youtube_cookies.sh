#!/bin/bash

# This script updates the youtube_cookies.txt file using yt-dlp
# It fetches fresh cookies from the Chrome browser for youtube.com

yt-dlp \
  --cookies-from-browser chrome \
  --cookies youtube_cookies.txt \
  --skip-download \
  "https://www.youtube.com/watch?v=1XF-NG_35NE" # A dummy URL to trigger cookie fetching

echo "YouTube cookies updated in youtube_cookies.txt"

echo "Rebuilding and restarting Docker container..."
docker-compose up --build -d
