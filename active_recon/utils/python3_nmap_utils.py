import socket
import ipaddress
import nmap3
from yellow_hat.constants import NMAP_SCAN_TYPES


def convert_domain_or_ip(user_input):
    try:
        ip_addr = ipaddress.ip_address(user_input)
        return str(ip_addr)
    except ValueError:
        try:
            ip_address = socket.gethostbyname(user_input)
            return ip_address
        except socket.gaierror:
            return None


def nmap_os_detection(host):
    # TODO: developing
    nmap = nmap3.Nmap()
    result = nmap.nmap_os_detection(host)
    return result


def nmap_dns_script_brute_force(host):
    # TODO: developing
    print("Call function nmap_dns_script_brute_force")
    nmap = nmap3.Nmap()

    # in case user input domain instead of ip address, call this function to get the ip
    ip_address = convert_domain_or_ip(host)

    if not ip_address:
        raise Exception("Issue with the domain or target ip that user input")

    # call nmap_dns_brute_script of nmap object
    result = nmap.nmap_dns_brute_script(ip_address)

    print(f"Result is: {result}")

    return result


def nmap_version_detection(host):
    print("Call function nmap_version_detection")
    nmap = nmap3.Nmap()

    # in case user input domain instead of ip address, call this function to get the ip
    ip_address = convert_domain_or_ip(host)

    if not ip_address:
        raise Exception("Issue with the domain or target ip that user input")

    # call nmap_version_detection of nmap object
    result = nmap.nmap_version_detection(ip_address)

    # Check if the result contains valid data
    if ip_address not in result:
        raise Exception("No valid scanning result for the given host.")

    # Extract the scanning result for the specified host
    scanning_info = result[ip_address]

    # Initialize a list to hold cleaned port data
    cleaned_ports_data = []

    # Extract necessary data from the scanning result
    for port in scanning_info.get("ports", []):
        port_data = {
            "portid": port.get("portid"),
            "protocol": port.get("protocol"),
            "state": port.get("state"),
            "reason": port.get("reason"),
            "service": {
                "name": port.get("service", {}).get("name", "unknown"),
                "product": port.get("service", {}).get("product", "unknown"),
                "version": port.get("service", {}).get("version", "unknown"),
                "extrainfo": port.get("service", {}).get("extrainfo", "unknown"),
                "ostype": port.get("service", {}).get("ostype", "unknown"),
            },
            "cpe": port.get("cpe", []),
        }
        cleaned_ports_data.append(port_data)

    # Construct the final result
    clean_result = {
        "ip": ip_address,
        "ports": cleaned_ports_data,
    }

    print(f"result inside nmap_version_detection is: {clean_result}")
    return clean_result


def nmap_tcp_syn_scan(host):
    # TODO: developing
    nmap = nmap3.NmapScanTechniques()
    result = nmap.nmap_syn_scan(host, arguments="--privileged")
    return result


def nmap_top_ports_scan(host):
    print("Call function nmap_top_ports_scan")
    nmap = nmap3.Nmap()

    # in case user input domain instead of ip address, call this function to get the ip
    ip_address = convert_domain_or_ip(host)

    if not ip_address:
        raise Exception("Issue with the domain or target ip that user input")

    result = nmap.scan_top_ports(ip_address, args="-sV")
    print(f"result is {result}")

    # Check if the result contains valid data
    if ip_address not in result:
        raise Exception("No valid scanning result for the given host.")

    # Extract the scanning result for the specified host
    scanning_info = result[ip_address]

    # Initialize a list to hold cleaned port data
    cleaned_ports_data = []

    # Extract necessary data from the scanning result
    for port in scanning_info.get("ports", []):
        port_data = {
            "portid": port.get("portid"),
            "protocol": port.get("protocol"),
            "state": port.get("state"),
            "reason": port.get("reason"),
            "service": port.get("service", {}).get("name", "Unknown"),
        }
        cleaned_ports_data.append(port_data)

    clean_result = {
        "ip": ip_address,
        "ports": cleaned_ports_data,
    }

    return clean_result


def is_valid_scan_type(scan_type_value):
    valid_scan_types = {scan_type["value"] for scan_type in NMAP_SCAN_TYPES}
    return scan_type_value in valid_scan_types


def get_scan_type_name(scan_type_value):
    for scan_type in NMAP_SCAN_TYPES:
        if scan_type["value"] == scan_type_value:
            return scan_type["name"]
    return None
