import socket
import ipaddress
import nmap3
import nmap
from yellow_hat.constants import NMAP_SCAN_TYPES
from concurrent.futures import ThreadPoolExecutor, as_completed


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


def nmap_scan(ip_address, scan_args):
    """Function to perform a scan on a given IP address."""
    nm = nmap.PortScanner()
    nm.scan(ip_address, arguments=scan_args)
    return nm


def scan_vulnerabilities_concurrent(
    host_domain, min_parallelism=10, max_parallelism=100
):
    # TODO: developing
    """Scan the given host for vulnerabilities using Nmap with concurrency."""
    print(f"Scanning {host_domain} for vulnerabilities")

    # Convert domain to IP address if needed
    ip_address = convert_domain_or_ip(host_domain)
    if not ip_address:
        raise Exception("Issue with the domain or target IP that user input")

    # Define the arguments for the scan
    scan_args = "-sV --script=vuln -T5"  # T4 for faster execution

    # Add parallelism options if specified
    if min_parallelism:
        scan_args += f" --min-parallelism {min_parallelism}"
    if max_parallelism:
        scan_args += f" --max-parallelism {max_parallelism}"

    # Perform the scan concurrently
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(nmap_scan, ip_address, scan_args)]
        results = []
        for future in as_completed(futures):
            nm = future.result()
            if ip_address in nm.all_hosts():
                for host in nm.all_hosts():
                    host_info = {
                        "host": host,
                        "hostname": nm[host].hostname(),
                        "state": nm[host].state(),
                        "protocols": [],
                    }
                    for proto in nm[host].all_protocols():
                        protocol_info = {"protocol": proto, "ports": []}
                        lport = nm[host][proto].keys()
                        for port in lport:
                            port_info = {
                                "port": port,
                                "state": nm[host][proto][port]["state"],
                                "scripts": nm[host][proto][port].get("script", {}),
                            }
                            protocol_info["ports"].append(port_info)
                        host_info["protocols"].append(protocol_info)
                    results.append(host_info)

    print(f"result is {results}")
    return results if results else None


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


def nmap_version_detection(host, min_parallelism=10, max_parallelism=100):
    print("Call function nmap_version_detection")
    nmap = nmap3.Nmap()

    # in case user input domain instead of ip address, call this function to get the ip
    ip_address = convert_domain_or_ip(host)

    if not ip_address:
        raise Exception("Issue with the domain or target ip that user input")

    # Define the arguments for the scan
    scan_args = "-T5"

    # Add parallelism options if specified
    if min_parallelism:
        scan_args += f" --min-parallelism {min_parallelism}"
    if max_parallelism:
        scan_args += f" --max-parallelism {max_parallelism}"

    # call nmap_version_detection of nmap object
    result = nmap.nmap_version_detection(ip_address, args=scan_args)

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


def nmap_top_ports_scan(host, min_parallelism=10, max_parallelism=100):
    print("Call function nmap_top_ports_scan")
    nmap = nmap3.Nmap()

    # in case user input domain instead of ip address, call this function to get the ip
    ip_address = convert_domain_or_ip(host)

    if not ip_address:
        raise Exception("Issue with the domain or target ip that user input")

    # Define the arguments for the scan
    scan_args = "-sV -T5"

    # Add parallelism options if specified
    if min_parallelism:
        scan_args += f" --min-parallelism {min_parallelism}"
    if max_parallelism:
        scan_args += f" --max-parallelism {max_parallelism}"

    result = nmap.scan_top_ports(ip_address, args=scan_args)
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
