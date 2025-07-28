# Dockerfile for the Anti-Ad FortiGuard Blocklist Exporter

# Use the official lightweight Python 3.11 image.
FROM python:3.11-slim

# Set the working directory inside the container.
WORKDIR /app

# Install the 'requests' library needed by the Python script.
RUN pip install --no-cache-dir requests

# Copy the Python script and the new entrypoint script into the container.
COPY fetch_domains.py .
COPY entrypoint.sh .

# Make the entrypoint script executable.
RUN chmod +x entrypoint.sh

# Set the entrypoint script as the command to run when the container starts.
CMD ["./entrypoint.sh"]
