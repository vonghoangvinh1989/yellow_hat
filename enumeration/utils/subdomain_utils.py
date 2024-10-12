import requests
from active_recon.utils.python3_nmap_utils import convert_domain_or_ip


def get_subdomains_securitytrails(domain, api_key):
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {"Accept": "application/json", "APIKEY": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        subdomains = [subdomain + "." + domain for subdomain in data["subdomains"]]
        return subdomains
    else:
        print(f"Error fetching subdomains from SecurityTrails: {response.status_code}")
        return []


def get_ip_address(subdomain, api_key):
    url = f"https://api.securitytrails.com/v1/domain/{subdomain}/dns"
    headers = {"Accept": "application/json", "APIKEY": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Extracting IP addresses from the A records
        a_records = data.get("records", {}).get("A", [])
        if a_records:
            return a_records[0].get("ip", "No IP found")
        else:
            return "No A records found"
    else:
        print(
            f"Error fetching IP for {subdomain} from SecurityTrails: {response.status_code}"
        )
        return "Error"


def enumerate_subdomains_securitytrails(domain, api_key):
    subdomains = get_subdomains_securitytrails(domain, api_key)
    result = []

    for subdomain in subdomains:
        ip_address = convert_domain_or_ip(subdomain)
        result.append({"subdomain": subdomain, "ip_address": ip_address})

    return result
