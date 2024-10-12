NSLOOKUP = ["nslookup"]
WHOIS = ["whois"]
NMAP = ["nmap"]
SNMP_WALK = ["snmpwalk"]
SUBDOMAIN = ["subdomain"]
EMAIL_FINDER = ["email-finder", "email finder"]

UDP_SCAN = "udp_scan"
TCP_SCAN = "tcp_scan"
SYN_SCAN = "syn_scan"
TCP_CONNECT_SCAN = "tcp_connect_scan"
AGGRESSIVE_SCAN = "aggressive_scan"
OS_DETECTION_SCAN = "os_detection_scan"
VERSION_DETECTION_SCAN = "version_detection_scan"
TOP_PORTS_SCAN = "top_ports_scan"

NMAP_SCAN_TYPES = [
    {
        "name": "Version Detection Scan",
        "value": VERSION_DETECTION_SCAN,
    },
    {
        "name": "Top Ports Scan",
        "value": TOP_PORTS_SCAN,
    },
]
