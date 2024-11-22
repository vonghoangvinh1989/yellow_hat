# from pysnmp.hlapi import *
# from pysnmp.entity import engine
from pysnmp.hlapi.v3arch.asyncio import *


async def snmp_walk(
    target, community, port=161, start_oid="1.3.6.1.2.1", timeout=1, retries=3
):
    # Initialize SNMP engine
    snmpEngine = SnmpEngine()  # Corrected import for SnmpEngine

    # Initialize the SNMP request
    iterator = getCmd(
        snmpEngine,
        CommunityData(community, mpModel=0),  # Using SNMP v1 (mpModel=0)
        await UdpTransportTarget.create(
            (target, port), timeout=timeout, retries=retries
        ),
        ContextData(),
        ObjectType(ObjectIdentity(start_oid)),
        lexicographicMode=False,
    )

    results = []

    try:
        # Execute the SNMP walk
        errorIndication, errorStatus, errorIndex, varBinds = await iterator

        # Check for errors in the response
        if errorIndication:
            print(f"Error: {errorIndication}")
        elif errorStatus:
            print(
                f"Error: {errorStatus.prettyPrint()} at {errorIndex if errorIndex else '?'}"
            )
        else:
            # Collect the results if no error
            for varBind in varBinds:
                results.append(" = ".join([x.prettyPrint() for x in varBind]))

    except Exception as e:
        print(f"Exception occurred: {str(e)}")

    finally:
        # Close the SNMP engine dispatcher
        snmpEngine.closeDispatcher()

    # Return the results as a list of strings
    print(f"Results: {results}")
    return results
