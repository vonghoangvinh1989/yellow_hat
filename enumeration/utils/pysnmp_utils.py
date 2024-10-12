from pysnmp.hlapi.v3arch.asyncio import *


async def snmp_walk(target, community, port=161, start_oid="1.3.6.1"):
    snmpEngine = SnmpEngine()

    iterator = getCmd(
        snmpEngine,
        CommunityData(community, mpModel=0),
        await UdpTransportTarget.create((target, port)),
        ContextData(),
        ObjectType(ObjectIdentity(start_oid)),
        lexicographicMode=False,
    )

    results = []

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        print("go here mean okay")
        for varBind in varBinds:
            results.append(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.closeDispatcher()

    print(f"results is: {results}")
    return results


import requests


def enumerate_subdomains_securitytrails(domain, api_key):
    print(f"Go to function enumerate_subdomains_securitytrails")
    """
    Enumerate subdomains of a given domain using the SecurityTrails API.

    Parameters:
        domain (str): The domain to enumerate subdomains for.
        api_key (str): Your SecurityTrails API key.

    Returns:
        list: A list of subdomains.
    """
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {"Accept": "application/json", "APIKEY": api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        subdomains = [subdomain + "." + domain for subdomain in data["subdomains"]]

        print(f"subdomains is: {subdomains}")

        return subdomains
    else:
        print(f"Error fetching subdomains from SecurityTrails: {response.status_code}")
        return []


# async def snmp_walk(target, community, port=161, start_oid="1.3.6.1"):
#     print("Call function snmp_walk")
#     """
#     Perform an SNMP walk operation to retrieve all information from the target device.

#     :param target: Target device IP address or hostname
#     :param community: SNMP community string
#     :param port: SNMP port, default is 161
#     :param start_oid: Starting OID for the SNMP walk, default is '1.3.6.1'
#     :return: A list of tuples containing OID and value
#     """
#     results = []
#     for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
#         SnmpEngine(),
#         CommunityData(community),
#         await UdpTransportTarget.create((target, port)),
#         ContextData(),
#         ObjectType(ObjectIdentity(start_oid)),
#         lexicographicMode=False,
#     ):
#         if errorIndication:
#             print(f"Error: {errorIndication}")
#             break
#         elif errorStatus:
#             print(f"Error: {errorStatus.prettyPrint()}")
#             break
#         else:
#             print(f"varBinds is {varBinds}")
#             for varBind in varBinds:
#                 results.append((str(varBind[0]), str(varBind[1])))

#     print(f"Results is: {results}")
#     return results
