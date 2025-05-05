#!/bin/bash

# Output directory (Windows path from WSL)
# OUTPUT_DIR="/mnt/c/Users/tonyp/learn/music"
OUTPUT_DIR="./downloaded"
LOG_FILE="./ytdlp_errors.log"

# Create the output directory if needed
mkdir -p "$OUTPUT_DIR"

# Function to download audio if not already downloaded
download_audio() {
    local url="$1"
    local filename

    # Use yt-dlp to get the output filename without downloading
    filename=$(yt-dlp --get-filename -f "ba" -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$url" 2>/dev/null)

    if [[ -f "$filename" ]]; then
        echo "⚠️  Skipping: Already downloaded — $(basename "$filename")"
    else
        echo "⬇️  Downloading: $url"
        if yt-dlp -f "ba" -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$url"; then
            # Print path of the downloaded file
            filename=$(yt-dlp --get-filename -f "ba" -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$url")
            echo "$filename"
        else
            echo "❌ Failed: $url" | tee -a "$LOG_FILE"
        fi
    fi

}

# Input validation
if [ -z "$1" ]; then
    echo "Usage:"
    echo "  $0 <YouTube-URL>"
    echo "  $0 <file-with-URLs.txt>"
    exit 1
fi

# Clear previous log
rm -f "$LOG_FILE"

# Check if input is a file (batch download)
if [ -f "$1" ]; then
    while IFS= read -r url; do
        [[ -n "$url" ]] && download_audio "$url"
    done < "$1"
else
    # Single URL
    download_audio "$1"
fi

echo "✅ Done! Files in: $OUTPUT_DIR"
[[ -f "$LOG_FILE" ]] && echo "⚠️  Some downloads failed. See: $LOG_FILE"
