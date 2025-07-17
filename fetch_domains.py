import requests
import re

def extract_adguard_domains(url):
    print("Fetching AdGuard filter...")
    response = requests.get(url)
    lines = response.text.splitlines()
    domains = set()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        match = re.match(r"^\|\|([a-z0-9.-]+)\^", line)
        if match:
            domains.add(match.group(1))

    return sorted(domains)

def extract_adaway_domains(url):
    print("Fetching AdAway hosts...")
    response = requests.get(url)
    lines = response.text.splitlines()
    domains = set()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] != "localhost":
            domains.add(parts[1])

    return sorted(domains)

def save_domains(domains, filename):
    with open(filename, "w") as f:
        for domain in domains:
            f.write(domain + "\n")
    print(f"Saved {len(domains)} domains to {filename}")

if __name__ == "__main__":
    adguard_url = "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/filter.txt"
    adaway_url = "https://adaway.org/hosts.txt"

    adguard_domains = extract_adguard_domains(adguard_url)
    save_domains(adguard_domains, "adguard_domains.txt")

    adaway_domains = extract_adaway_domains(adaway_url)
    save_domains(adaway_domains, "adaway_domains.txt")
