import ipaddress

from fastapi import APIRouter, HTTPException
from services.networkservices import WNET

router = APIRouter(tags=["Network"])

network_service = WNET()


def is_valid_ip(ip: str) -> bool:
    """Validate IP address using Python's ipaddress module."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


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
        if is_valid_ip(target):
            network_service.pingo(target)
            return {"message": "Host is up"}
        else:
            return {"message": "Invalid IP address"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hostdiscovery/${interface}")
async def host_discovery(interface: str):
    try:
        print("Performing host discovery")
        discovered_devices = network_service.host_discovery(interface)

        # Implement host discovery logic here
        return {"message": "Host discovery completed", "data": discovered_devices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
