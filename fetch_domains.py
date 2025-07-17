"""
Fetches, parses, and saves domain blocklists from various sources to make them
compatible with FortiGate's External Block List (Threat Feed) feature.
"""
import requests
import re

def fetch_and_parse_list(name, url, parser_func):
    """
    Fetches a list from a URL, parses it using a provided function, and returns a set of domains.

    Args:
        name (str): A friendly name for the list source (for logging).
        url (str): The URL of the blocklist to download.
        parser_func (function): The specific parser function to use for the list format.

    Returns:
        set: A set of unique domain names from the list. Returns an empty set on failure.
    """
    print(f"Fetching {name} from {url}...")
    domains = set()
    try:
        # Make an HTTP GET request to the URL with a 15-second timeout.
        response = requests.get(url, timeout=15)
        # Raise an exception if the HTTP response indicates an error (e.g., 404, 500).
        response.raise_for_status()
        
        # Pass the downloaded text to the appropriate parser function.
        domains = parser_func(response.text)
        print(f"Successfully parsed {len(domains)} domains from {name}.")
    except requests.exceptions.RequestException as e:
        # Catch any network-related errors during the download.
        print(f"Error fetching {name}: {e}")
    return domains

def parse_adguard_filter(text):
    """
    Parses text in the AdGuard/Adblock Plus filter format (e.g., ||example.com^).

    Args:
        text (str): The raw text content of the filter list.

    Returns:
        set: A set of extracted domain names.
    """
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        # We are only interested in lines that block entire domains.
        if line.startswith("||") and line.endswith("^"):
            # Use regex to extract the domain part.
            match = re.match(r"^\|\|([a-z0-9.-]+)\^", line)
            if match:
                domains.add(match.group(1))
    return domains

def parse_hosts_file(text):
    """
    Parses text in the standard hosts file format (e.g., 0.0.0.0 example.com).

    Args:
        text (str): The raw text content of the hosts file.

    Returns:
        set: A set of extracted domain names.
    """
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        # Ignore empty lines and comments.
        if not line or line.startswith("#"):
            continue
        
        parts = line.split()
        # Ensure the line has at least two parts (IP and domain) and is a blocking rule.
        if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"):
            domains.add(parts[1])
    return domains

def save_domains(domains, filename):
    """
    Saves a set of domains to a specified file, with one domain per line.

    Args:
        domains (set): The set of domains to save.
        filename (str): The name of the output file.
    """
    with open(filename, "w") as f:
        # Sort the domains alphabetically before writing for consistency.
        for domain in sorted(list(domains)):
            f.write(domain + "\n")
    print(f"Saved {len(domains)} domains to {filename}")

# This standard Python construct ensures the code inside only runs when the script
# is executed directly (not when imported as a module).
if __name__ == "__main__":
    # --- Source 1: AdGuard DNS Filter ---
    adguard_domains = fetch_and_parse_list(
        "AdGuard DNS filter",
        "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/adguard-sdns-filter.txt",
        parse_adguard_filter
    )
    save_domains(adguard_domains, "adguard_domains.txt")

    # --- Source 2: AdAway Hosts List ---
    adaway_domains = fetch_and_parse_list(
        "AdAway hosts",
        "https://adaway.org/hosts.txt",
        parse_hosts_file
    )
    save_domains(adaway_domains, "adaway_domains.txt")
