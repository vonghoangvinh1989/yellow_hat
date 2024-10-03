from celery import shared_task
import whois


def scan_whois(domain):
    result = f"TARGET DOMAIN: {domain}\n\n"

    whois_object = whois.whois(domain)
    result = whois_object.text

    print(f"Result is {result}")

    return result
