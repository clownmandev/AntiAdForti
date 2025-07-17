import requests
import re

def fetch_and_parse_list(name, url, parser_func):
    """Fetches a list, parses it, and returns a set of domains."""
    print(f"Fetching {name} from {url}...")
    domains = set()
    try:
        response = requests.get(url, timeout=15)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        domains = parser_func(response.text)
        print(f"Successfully parsed {len(domains)} domains from {name}.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {name}: {e}")
    return domains

def parse_adguard_filter(text):
    """Parses AdGuard/Adblock-style filter text."""
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("||") and line.endswith("^"):
            match = re.match(r"^\|\|([a-z0-9.-]+)\^", line)
            if match:
                domains.add(match.group(1))
    return domains

def parse_hosts_file(text):
    """Parses a hosts-file-style text."""
    domains = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"):
            domains.add(parts[1])
    return domains

def save_domains(domains, filename):
    """Saves a list of domains to a file."""
    with open(filename, "w") as f:
        for domain in sorted(list(domains)):
            f.write(domain + "\n")
    print(f"Saved {len(domains)} domains to {filename}")

if __name__ == "__main__":
    adguard_domains = fetch_and_parse_list(
        "AdGuard DNS filter",
        "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/filter.txt",
        parse_adguard_filter
    )
    save_domains(adguard_domains, "adguard_domains.txt")

    adaway_domains = fetch_and_parse_list(
        "AdAway hosts",
        "https://adaway.org/hosts.txt",
        parse_hosts_file
    )
    save_domains(adaway_domains, "adaway_domains.txt")