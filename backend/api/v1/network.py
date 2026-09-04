import re
import socket
from fastapi import APIRouter, HTTPException
from backend.services.networkservices import WNET
import ipaddress
router = APIRouter(tags=["Network"])

network_service = WNET()

ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/interfaces")
async def get_host_interfaces():
    try:
        print("Getting network interfaces")
        # interfaces = network_service.get_interfaces()
        print(network_service.interfaces)
        # Implement network interface retrieval logic here
        return {
            "message": "Network interfaces retrieved",
            "data": network_service.interfaces,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ping/{target}")
async def ping(target: str):
    try:
        if ip_pattern.match(target):
            # print(f"Pinging {target}")
            network_service.pingo(target)
            return {"message": "Host is up"}
        else:
            return {"message": "Invalid IP address"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hostdiscovery/{interface}")
async def host_discovery(interface: str):
    try:
        print("Performing host discovery")
        discovered_devices = network_service.host_discovery(interface)

        # Implement host discovery logic here
        return {"message": "Host discovery completed", "data": discovered_devices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        # Single port scan

@router.get("/sscan/{target_ip}/{port}")
async def single_port_scan(target_ip:str,port:int):
    try:
        print(target_ip)
        ipaddress.IPv4Address(target_ip)
        
        port_status = network_service.single_portscan(target_ip,port)
        print(port_status)
        return { "details": port_status }
    except ipaddress.AddressValueError:
        raise HTTPException(status_code=400,detail=f"Invalid ipv4 addess")
    except Exception as e:
        return {"error":f"{e}"}



    # common port scan
@router.get("cscan/{target_ip}")
async def common_port_scan(target_ip:str):
    try:
        print(target_ip)
        message = network_service.multi_portscan(target_ip)
        return {"message ": "Successful" , "Port status": message}
    except ipaddress.AddressValueError:
        raise HTTPException(status_code=404,detail="Invalid Ip address")


# Os detection
@router.get("oscan/{target_ip}")
async def os_detection():
    return {"Detected OS":"Linux"}

