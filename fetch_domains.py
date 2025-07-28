if __name__ == "__main__":
    # --- Define all blocklist sources here ---
    # The first "AdGuard DNS Filter" source has been removed as the URL is invalid (404).
    sources = [
        {
            "name": "AdAway Hosts",
            "url": "https://adaway.org/hosts.txt",
            "parser": parse_hosts_file
        },
        {
            "name": "AdGuard Base AdServers",
            "url": "https://adguardteam.github.io/AdguardFilters/BaseFilter/sections/adservers.txt",
            "parser": parse_adguard_filter
        },
        {
            "name": "EasyList AdServers",
            "url": "https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_adservers.txt",
            "parser": parse_adguard_filter
        },
        {
            "name": "AdGuard SDNSFilter Full",
            "url": "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt",
            "parser": parse_adguard_filter
        }
    ]

    # --- Fetch, parse, and save each list individually ---
    for source in sources:
        # Fetch and parse the current list
        domains = fetch_and_parse_list(source["name"], source["url"], source["parser"])

        # Generate a clean filename from the source name
        # (e.g., "AdAway Hosts" becomes "adaway_hosts.txt")
        output_filename = source["name"].lower().replace(" ", "_") + ".txt"
        
        # Save the domains to their own file
        save_domains(domains, output_filename)
