import requests


def get_all_info_from_domain(domain, api_key):
    print("Go to function get_all_info_from_domain")
    """
    Fetch all information associated with a specified domain using Hunter.io API.

    Args:
        domain (str): The domain to search for information (e.g., 'example.com').
        api_key (str): Your Hunter.io API key.

    Returns:
        dict: A dictionary containing all information found for the specified domain.
    """
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "api_key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        data = response.json()

        # Extract all relevant information from the response
        info = {
            "domain": data.get("data", {}).get("domain", ""),
            "emails": data.get("data", {}).get("emails", []),
            "company": data.get("data", {}).get("company", ""),
            "address": data.get("data", {}).get("address", ""),
            "country": data.get("data", {}).get("country", ""),
            "phone": data.get("data", {}).get("phone", ""),
            "social_profiles": data.get("data", {}).get("social_profiles", []),
            "sources": data.get("data", {}).get("sources", []),
            "status": data.get("data", {}).get("status", ""),
        }

        return info
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return {}
