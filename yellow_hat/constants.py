NORMAL_CATEGORIES = [
    "Planning and Scoping Reports",
    "Passive Reconnaissance Reports",
    "Active Reconnaissance Reports",
    "Vulnerability Assessment Reports",
    "Enumeration Reports",
    "Digital Forensic Reports",
    "Other Reports",
]

MERGE_CATEGORIES = ["Merge Reports"]

NSLOOKUP = ["nslookup"]
WHOIS = ["whois"]
NMAP = ["nmap"]
SNMP_WALK = ["snmpwalk"]
SUBDOMAIN = ["subdomain"]
EMAIL_FINDER = ["email-finder"]

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

# For sign-up custom form
JOB_CHOICES = [
    ("", "Select your job role"),
    ("student", "Student"),
    ("developer", "Developer"),
    ("sysadmin", "System Administrator"),
    ("security", "Security Specialist"),
    ("manager", "IT Manager"),
    ("consultant", "Consultant"),
    ("other", "Other"),
]

# For digital forensic tool
VOLATILITY = ["volatility"]
REGIPY = ["regipy"]

# For exploitation
NMAP_SMB_BRUTE = ["nmap-smb-brute", "nmap smb-brute"]
PARAMIKO_SSH_BRUTE = ["paramiko-ssh-brute", "Paramiko SSH Brute", "paramiko ssh brute"]

# For post exploitation
LINPEAS = ["linpeas"]
