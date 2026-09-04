import ipaddress
import logging
import os
import platform
import socket
import subprocess
import re 
from scapy.all import ARP, Ether, conf, srp
import logging
regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


class WNET:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.interfaces = []
        self.get_interfaces()
        self.interface = None

    def pingo(self, host):

        param = "-n" if platform.platform().lower() == "win32" else "-c"
        # print(self.interfaces)
        # hostname = "google1.com"
        # response = os.system(f"ping {param} 1 {host}")
        response = subprocess.run(["ping",param,"1",host],capture_output=True,text=True)
        
        # print(f"Response code :{response.returncode}")
        if response.returncode == 0:
            return {"message": "Alive"}
        else:
            # print(f"Error: {response}")
            raise Exception("Ping failed")

    def get_interfaces(self):
        for iface_name in conf.ifaces:
            # print(iface_name)
            iface = conf.ifaces[iface_name]
            iface_data = {
                "index": iface.index,
                "name": iface.name,
                "mac": iface.mac,
                "ip": iface.ip or "Not Connected",
            }
            # print(iface_data)
            self.interfaces.append(iface_data)
        # print(self.interfaces)
        return self.interfaces

        # print(iface.name)

    def host_discovery(self, interface):
        # 1. Find the interface in self.interfaces
        interf = next(
            (intef for intef in self.interfaces if intef["name"] == interface), None
        )

        if not interf or interf["ip"] == "Not Connected":
            raise Exception("Interface not found or not connected")

        # 2. FIX: Added the '.0' before the /24.
        # Scapy needs 192.168.1.0/24, not 192.168.1/24
        ip_parts = interf["ip"].split(".")
        network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"

        # 3. Craft packets
        broadcast_address = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = ARP(pdst=network_range)
        arp_request = broadcast_address / arp

        print(f"Scanning {network_range} from interface {interface} ...")

        # 4. FIX: Correct unpacking.
        # srp returns a tuple (answered, unanswered).
        # Your previous code srp(...)[0] extracted 'answered' then tried to unpack it again.
        answered, unanswered = srp(
            arp_request, timeout=3, iface=interface, verbose=False
        )

        # 5. Process the results
        discovered_devices = []
        if answered:
            for sent, received in answered:
                device_info = {"ip": received.psrc, "mac": received.hwsrc}
                discovered_devices.append(device_info)
                print(f"Found: {device_info['ip']} at {device_info['mac']}")

            return discovered_devices
        else:
            print("No devices found.")
            raise Exception("No devices found.")

    def single_portscan(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        if (port < 1 or port > 65535):
            raise ValueError(f"nvalid port number {port}. Port number must be between  1 and 65535")
        result = s.connect_ex((ip, port))

        banner = ""
        if result == 0:  # Only recv if port is open
            try:
                banner = s.recv(1024).decode().strip()
            except Exception:
                pass  # Timeout or no banner received

        print(f"Banner: {banner}")
        print(f"Port {port} on {ip} is {'open' if result == 0 else 'closed'}")
        s.close()
        return {"port":port ,"status":"open" if result == 0 else "closed","banner":banner}
        #return result == 0

    def validate_ip(self,ip):
        if(re.search(regex,ip)):
            print("Valid Address")
            return True
        else:
            print("Invalid Ip ")
            return False

    def multi_portscan(self,ip:str):
        """
        Scans for common ports
        """
        common_ports = [21,22,25,80,8080,8000] 
        open_ports = []

        tasks = [self.single_portscan(ip,port) for port in common_ports]

        print("Tasks :")
        print(tasks)


        print("Multi Port scan")

        return tasks

    


if __name__ == "__main__":
    wnet = WNET()
    wnet.single_portscan("192.168.1.1", 80)
