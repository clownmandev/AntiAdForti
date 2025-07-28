#!/bin/sh

# Run the script once on startup to ensure the lists exist immediately.
echo "--- Performing initial domain fetch... ---"
python3 fetch_domains.py
echo "--- Initial fetch complete. Starting web server. ---"

# Start the built-in Python web server in the background on port 8080.
python3 -m http.server 8080 &

# Start the update loop. This will be the main process keeping the container alive.
# It sleeps first, then updates the files every 24 hours (86400 seconds).
echo "--- Update loop started. Next update in 24 hours. ---"
while true; do
  sleep 86400
  echo "--- [$(date)] Updating blocklists... ---"
  python3 fetch_domains.py
done
