#!/bin/bash

# This script updates the youtube_cookies.txt file using yt-dlp
# It fetches fresh cookies from the Chrome browser for youtube.com
echo "YouTube cookies updating using youtube_cookies.txt"

echo "Rebuilding and restarting Docker container..."
docker-compose up --build -d
