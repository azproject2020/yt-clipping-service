#!/bin/bash

# This script updates the youtube_cookies.txt file using yt-dlp
# It fetches fresh cookies from the Chrome browser for youtube.com
echo "Attempting to extract cookies from Chrome..."

yt-dlp --ignore-config --cookies-from-browser chrome --dump-cookies youtube_cookies.txt

if [ -s youtube_cookies.txt ]; then
    echo "youtube_cookies.txt updated successfully."
else
    echo "Failed to extract cookies or youtube_cookies.txt is empty. Please check yt-dlp output and ensure Chrome is not running or try the manual method."
    # Optionally, exit here if cookie extraction is critical
    # exit 1
fi

echo "Rebuilding and restarting Docker container..."
docker-compose up --build -d
