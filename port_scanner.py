# PORT SCANNER MODULE FOR // MAIN MODULE

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()


# NETWORK IMPORTS
from scapy.all import sniff
import socket


# ETC IMPORTS
from datetime import datetime
import time, threading


# FILE HANDLING
from pathlib import Path

# FILE DIRECTORY
base_dir = Path.home() / "Documents" / "nsm tools" / ".data" / "NetSniffer" / "common_port_scan_results"
base_dir.mkdir(parents=True, exist_ok=True)




class Common_port_scan():
    """This class will be responsible for performing a common port scan on on a device"""


    def __init__(self):
        self.open_ports = []
        self.filtered_ports = []
        self.closed_ports = []
        self.filtered_ports_no_service = 0
        pass


    def port_scan(self, ip: str, port: int):
        """This will scan a port"""

        known_ports = {
                465: "smtp",
                587: "smtp",
                2053: "cloudflare",
                2082: "cPanel",
                2083: "cPanel",
                2086: "whm",
                2087: "whm",
                2052: "clearVisn Services",
                2095: "cPanel Webmail",
                2096: "cPanel Webmail",
                2087: "cPanel whm",
                8080: "Http Alternative",
                8443: "Https Alternative",
                8880: "Http Alternative"
            }
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((ip, port))
                
                # CHECKS IF PORT IS OPEN, FILTERED OR CLOSED !
                if result == 0:
                    #console.print(f"{port} is [bold green]open[/bold green]")
                    
                    # DEFAULT TO COMMON SERVICE IF WE CANT FIND IT
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = known_ports.get(port, "unkown")
                    
                    status = "Open"
                    info = (f"Port: {port}   Service: {service}  Status: {status}")
                    self.open_ports.append(info)
                
                elif result in [111, 113]:
                   # console.print(f"{port} is [bold red]filtered[/bold red]")
                    
                    status = "Closed"
                    info = f"{port} {status}"
                    self.closed_ports.append(info)
                
                else:
                   # console.print(f"{port} is [yellow]filtered[/yellow]")

                    # DEFAULT TO COMMON SERVICE IF WE CANT FIND IT
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = known_ports.get(port, "N/A")
                        self.filtered_ports_no_service += 1
                        return
                    
                    status = "Filtered"
                    info = (f"Port:  {port}  Service:  {service}  Status: {status}")
                    self.filtered_ports.append(info)
                
    
        except Exception as e:
            console.print(e, port)
    

    def threader(self, ip):
        """Will create a thread for each port to then scan for faster results"""

        ports = range(1, 1025)
        threads = []

        for port in ports:
            t = threading.Thread(target=self.port_scan, args= (ip, port), daemon=True)
            threads.append(t)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
    
    def scanner(self, ip: str, mac:str, host, vendor):
        """User will enter device info for a scan to begin"""

        self.threader(ip)
        self.save_results(ip, mac, host, vendor)
    

    def save_results(self, ip: str, mac: str, host, vendor):
        """Responsible for saving scan results"""
        
        # SPLIT IP AND TURN IT INTO A TXT PATH
        ip_path = '_'.join(ip.split('.'))
        file_path = base_dir / f"{ip_path}.txt"


        # WELCOME MESSAGE // DEVICE INFO 
        time_stamp = datetime.now().strftime("%m-%d-%Y  %H:%M:%S")       
        welcome = f"Welcome to NetSniffer  -  Created by Bari\n\nTimeStamp: {time_stamp}"
        device_info = f"\nIP Address: {ip} / MAC Address: {mac} / Host Name: {host} / Vendor: {vendor}"


        # TO ORGANIZE DATA NOW
        opened = "\n".join(self.open_ports)
        filtered = "\n".join(self.filtered_ports)
        closed = "\n".join(self.closed_ports)

        show = False


        if show:
        # OPEN
            console.print(opened)
            console.print(f"\nOpen Ports: {len(self.open_ports)}")

            # FILTERED
            print("\n\n")
            console.print(filtered)
            self.filtered_ports_no_service += len(self.filtered_ports)
            
            console.print(f"\n\nFiltered Ports with Service: {len(self.filtered_ports)}")
            console.print(f"Total Filtered Ports: {self.filtered_ports_no_service}")
            # CLOSED
            print("\n\n")
            console.print(closed)
            console.print(f"Closed Ports: {len(self.closed_ports)}")


        # NOW TO ADD DATA TO A TXT FILE
        data = f"{opened}\n\nOpen Ports: {len(self.open_ports)}\n-----------------------------------------------------------------------\n\n {filtered}\n\nFiltered Ports with Service: {len(self.filtered_ports)}\nTotal Filtered Ports: {self.filtered_ports_no_service}\n-----------------------------------------------------------------------\n\nClosed Ports: {len(self.closed_ports)}"


        log_format = f"{welcome}\n\n{device_info}\n\n\n{data}"

        
        try:
            with open(file_path, "w") as file:
                file.write(log_format)
                console.print(f'{ip}: Done')
        
        except Exception as e:
            console.print(e)




# STRICTLY FOR MODULE TESTING
if __name__ == "__main__":

    ip = "192.168.1.38"
    mac = ""
    host = ""
    vendor = ""

    Common_port_scan().scanner(ip, mac, host, vendor)

