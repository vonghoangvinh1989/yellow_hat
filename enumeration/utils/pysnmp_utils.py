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
