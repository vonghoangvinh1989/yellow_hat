import nmap3
from yellow_hat.constants import NMAP_SCAN_TYPES


def nmap_os_detection(host):
    nmap = nmap3.Nmap()
    result = nmap.nmap_os_detection(host)
    return result


def nmap_version_detection(host):
    nmap = nmap3.Nmap()
    result = nmap.nmap_version_detection(host)
    return result


def nmap_tcp_syn_scan(host):
    nmap = nmap3.NmapScanTechniques()
    result = nmap.nmap_syn_scan(host, arguments="--privileged")
    return result


def nmap_top_ports_scan(host):
    print("Call function nmap_top_ports_scan")
    nmap = nmap3.Nmap()
    result = nmap.scan_top_ports(host, args="-sV")

    # Check if the result contains valid data
    # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
    if host not in result:
        raise Exception("No valid scanning result for the given host.")

    # Extract the scanning result for the specified host
    scanning_info = result[host]

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

    return {
        "ip": host,
        "ports": cleaned_ports_data,
        "hostname": scanning_info.get("hostname", [{}])[0].get("name", "Unknown"),
    }


def is_valid_scan_type(scan_type_value):
    valid_scan_types = {scan_type["value"] for scan_type in NMAP_SCAN_TYPES}
    return scan_type_value in valid_scan_types


def get_scan_type_name(scan_type_value):
    for scan_type in NMAP_SCAN_TYPES:
        if scan_type["value"] == scan_type_value:
            return scan_type["name"]
    return None
