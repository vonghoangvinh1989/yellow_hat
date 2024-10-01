import dns.resolver


def scan_domain(domain):
    ids = [
        "A",
        "NS",
        "CNAME",
        "AAAA",
        "MX",
        "SOA",
        "PTR",
        "TXT",
        "DNSKEY",
        "AXFR",
    ]

    result = f"TARGET DOMAIN: {domain}\n\n"
    for item in ids:
        result += f"----------- {item.upper()} -----------\n"
        try:
            answers = dns.resolver.query(domain, item)
            for rdata in answers:
                result += f"{item}: {rdata.to_text(sorted=True,want_comments=True)}\n"
            result += f"---------------------------\n\n"
        except Exception as error:
            result += f"Reason: {error}\n"
            result += f"---------------------------\n\n"
    return result
