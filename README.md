# Anti-Ad FortiGuard Blocklist Exporter

This project provides a simple, self-hosted Docker container that automatically fetches popular ad-blocking lists and makes them compatible with a FortiGate firewall's **External Block List (Threat Feed)** feature.

It downloads, parses, and serves domain-only lists from:
- **AdGuard DNS Filter**
- **AdAway Hosts List**

This allows you to implement robust, network-wide ad and tracker blocking on every device protected by your FortiGate, without needing to install any client-side software.

## How It Works

1.  A Python script (`fetch_domains.py`) runs inside a Docker container.
2.  The script downloads the latest AdGuard and AdAway blocklists.
3.  It strips away all non-domain syntax (like `||`, `^`, comments, etc.), creating clean lists of just domains.
4.  It saves the lists as `adguard_domains.txt` and `adaway_domains.txt`.
5.  A simple Python web server serves these text files over HTTP on a local port.
6.  The script automatically re-downloads the lists every 24 hours to keep them up-to-date.

## Requirements
* Docker and Docker Compose installed.
* Portainer (optional, but recommended for easy management).
* A FortiGate firewall.

## Quick Start: Deployment with Portainer

1.  **Go to Stacks** -> **Add Stack**.
2.  **Select "Git Repository"** as the build method.
3.  **Repository URL:** `https://github.com/clownmandev/AntiAdForti`
4.  **Compose path:** `docker-compose.yml`
5.  Click **Deploy the stack**.

## Manual Deployment

1.  Clone this repository:
    ```sh
    git clone [https://github.com/clownmandev/AntiAdForti.git](https://github.com/clownmandev/AntiAdForti.git)
    cd AntiAdForti
    ```
2.  Build and run the container:
    ```sh
    docker-compose up -d
    ```

## FortiGate Configuration

Once the container is running, configure your FortiGate to use the generated lists.

1.  **Create External Connectors:**
    * Navigate to **Security Fabric** -> **External Connectors**.
    * Create a new **Domain Name** Threat Feed for each list:
        * **Name:** `AdGuard-Custom-List`
        * **URL:** `http://<your-docker-host-ip>:8080/adguard_domains.txt`
        * **Refresh Rate:** `1440` minutes (24 hours)
    * Repeat for the AdAway list:
        * **Name:** `AdAway-Custom-List`
        * **URL:** `http://<your-docker-host-ip>:8080/adaway_domains.txt`

2.  **Apply to a DNS Filter:**
    * Navigate to **Security Profiles** -> **DNS Filter**.
    * Edit your primary profile.
    * Under **External Malware Block Lists**, enable the two connectors you just created.

3.  **Enable on a Firewall Policy:**
    * Navigate to **Policy & Objects** -> **Firewall Policy**.
    * Edit your main LAN-to-WAN policy and enable the **DNS Filter** security profile.

Your FortiGate will now block DNS requests for domains found on these lists across your entire network.
