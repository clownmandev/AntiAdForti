#
# Dockerfile for the Anti-Ad FortiGuard Blocklist Exporter
# This file defines the steps to build the Docker image.
#

# Use the official lightweight Python 3.11 image as the base. 'slim' is a
# smaller variant, resulting in a more efficient final image.
FROM python:3.11-slim

# Set the working directory inside the container to /app. All subsequent commands
# will run from this directory.
WORKDIR /app

# Install the 'requests' library, which is needed by the Python script to make
# HTTP requests to download the blocklists. The --no-cache-dir flag prevents
# pip from storing the installation cache, keeping the image size smaller.
RUN pip install --no-cache-dir requests

# Copy the Python script from your local machine (the build context) into the
# container's working directory (/app).
COPY fetch_domains.py .

# Create a small startup script for the web server and make it executable.
# This makes the final CMD line cleaner and easier to read.
RUN echo 'python3 -m http.server 8080' > start.sh && chmod +x start.sh

# This is the main command that runs when the container starts. It does two things:
# 1. `while true; ...; done &`: It starts an infinite loop in the background (`&`).
#    This loop runs the fetch_domains.py script, then sleeps for 86400 seconds
#    (24 hours) before repeating. This keeps the lists updated daily.
# 2. `./start.sh`: While the update loop runs in the background, this command
#    immediately starts the web server to serve the files.
CMD ["sh", "-c", "while true; do python3 fetch_domains.py; sleep 86400; done & ./start.sh"]
