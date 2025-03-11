# PACKET INSPECTION MODULE FOR // MAIN MODULE 
# THIS MODULE IS RESPONSIBLE FOR CAPTURING AND OR MANIPULATING PACKETS TRAVERSE THE LAN 


# OTHER MODULE IMPORTS

 


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()


# NETWORK IMPORTS
from scapy.all import sniff


# ETC IMPORTS
from datetime import datetime
import time


# FILE HANDLING
from pathlib import Path

# FILE DIRECTORY
base_dir = Path.home() / "Documents" / "nsm tools" / ".data" / "NetSniffer" / "IP Packet Logging"
base_dir.mkdir(parents=True, exist_ok=True)



class packet_capture():
    """This class will be responsible for capturing network traffic and potentially manipulating it """


    def __init__(self):
        pass

    def sniffer(self, ip: str, mac: str, host, vendor):
        """This method will sniff network traffic"""

        
        # FUNCTION WITHIN A METHOD FOR BETTER MODULARITY 
        def save_traffic(pkt):
            """This method will save said traffic found traversing the network"""

            try:

                pkt_data = pkt.summary()
                ip_logging().ip_logger(ip, mac, host, vendor,  data=pkt_data)

            
            except Exception as e:
                console.print(f"[bold red]Error processing packet:[/bold red] {e}")
            


        sniff(filter=f"host {ip}", prn=save_traffic)
    

    def active_count(self):
        """Count for ip logging count"""
        pass



class ip_logging():
    """This class will be responsible for logging traffic"""

    def __init__(self):
        pass
    

    def ip_logger(self, ip: str, mac: str, host, vendor, data):
        """This will log traffic to a text file"""

        
        # LOOP IN CASE OF EXCEPTION ERRORS
        
        try:

            # CREATE THE DYNAMIC FILE PATH FOR IP
            ip_path = '_'.join(ip.split('.'))
            file_path = base_dir / f"{ip_path}.txt"
            time_stamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            log_format = f"Timestamp: {time_stamp} - {data}\n"


            # SINCE WERE USING EXIST_OK GLOBALY WE CANT NORMALLY USE FILENOTFOUNDERROR
            if file_path.exists():

                with open(f"{file_path}", "a") as file:
                    file.write(log_format)

            else:

                default = f"Welcome to NetSniffer, Created by Bari\n\nIP Logging ----> IP Address: {ip} / MAC Address: {mac} / Host name: {host} / Vendor: {vendor}\n\n\n"

                with open(f"{file_path}", "w") as file:
                    file.write(default) 

                console.print(f"[bold red]Default file path with:[/bold red] {ip}[bold green] successfully created[/bold green]")
            
        except Exception as e:
            console.print(e)

    
    def device_count(self, count, devices):
        """This program will be responsible for keeping track of the amount of online devices and updating it within a text file"""
        
        try:


            
            msg = f"Total Devices Found: {devices}"
            msgg = f"Total_Devices_Found_{count}"
            console.print(msg)



            file_path = base_dir / f"{msgg}.txt"
            
            with open(file_path, "w") as file:
                file.write(msg)
        
        except Exception as e:
            console.print(e)

            
