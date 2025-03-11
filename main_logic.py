# IP SNIFFER // NetSniffer


# OTHER MODULE IMPORTS
from packet_inspection import packet_capture, ip_logging
from port_scanner import Common_port_scan


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()


# NETWORK IMPORTS
from scapy.all import sniff, IP, ICMP, srp, sr1, Ether, ARP
import socket, ipaddress


# ETC IMPORTS
import threading, random, requests, asyncio, json, time



# FILE MODULE IMPORTS
from utilities import Utilities



class network_sniffer():
    """This class will scan and then procceed to sniff network traffic and monitor device status"""


    def __init__(self):
        self.speak = Utilities()
        self.lock = threading.Lock()
        pass

    def pinger(self, ip, mac, vendor):
        """This will be responsible for pining all the devices on your local network that are found from the subnet_scanner class and then pass to this class"""

        # SET BASE VARIABLES
        online = False
        first = True
        sleep = 10
        gateway_ip = "192.168.1.1"


        # LOOP THROUGH PINGING THE DEVICE
        while True:

            ping = IP(dst=ip) / ICMP() 

            response = sr1(ping, verbose=False, timeout=5, retry=3)   # SET THE RETRY TO 3 SO WE CAN REATTEMPT INSTEAD OF CAUSING A EXCEPTION ERROR
             
            
            # IF THE DEVICE IS FOUND NEWLY ONLINE WILL NOTIFY USER
            if response:

                if online == False:
                    host = Utilities().get_host(ip)
                    if first != True:

                        # USE THIS TO PREVENT RACE CONDITIONING ERRORS
                        with self.lock:
                            announce = Utilities().get_name(vendor, host, ip)
                            self.speak.tts(say=f"{announce} is now online")

                    console.print(f"{host} --> {vendor} --> {ip} is online")
                    online = True
                    first = False
                    sleep = 10
                    start_time = time.time()
            
            # IF FORMERLY ONLINE DEVICE IS NOW OFFLINE WILL NOTIFY USER
            elif online:

                # USE THIS TO PREVENT RACE CONDITIONING ERRORS
                with self.lock:
                    announce = Utilities().get_name(vendor, host, ip)
                    self.speak.tts(say=f"{announce} is now offline")

                online = False
                session_duration = time.time() - start_time
                #time_format = self.speak.get_time(session_duration)
                console.print(f"{host} --> {vendor} --> {ip} is offline, with a total session length of : {session_duration:.2f} seconds")      


                # TESTING

              #  ip_logging().device_count()      
            
            # THIS WILL PREVENT TERMINAL FROM REPEATEDLY NOTIFYING USERS WHEN THE DEVICE IS FORMERLY OFFLINE AND IS STILL OFFLINE
            else:
                
                # SIMPLE METHOD WERE IF THE DEVICE IS CONTINOUSLY PINGED AS OFFLINE WE WILL INCREASE TIME UNTIL NEXT PING TO NOT OVERWHELM THE NETWORK
                if sleep == 50:
                    sleep = 50

                else:

                    sleep += 5
            
            
            # NOW TO WAIT ON THE SLEEP VARIABLE BEFORE PERFORMING THE NEXT PING
            time.sleep(sleep)
        
    

class subnet_scanner():
    """This class will scan the network for active devices and then forward the results to the next class"""

    def __init__(self):
        self.active_devices = []
        self.sniffer = network_sniffer()
        self.exe = Utilities()
        pass


    def get_subnet(self):
        """Get a valid subnet to scan"""

        while True:
            try:
                subnet = console.input("[bold green]Enter subnet: [/bold green]")
                
                # TEMPORARY FOR CONTINOUS TESTING
                if subnet == "":
                    subnet = "192.168.1.0/24"

                valid_subnet = ipaddress.ip_network(subnet)
                return valid_subnet
            
            except ValueError as e:
                console.print(e)
            
            except ipaddress.AddressValueError as e:
                console.print(e)
            
            except ipaddress.NetmaskValueError as e:
                console.print(e)



    def arp_scanner(self, ip):
        """Will send arp request to devices on your subnet"""

        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(ip))

        response = srp(packet, verbose=False, timeout=3)[0]

        for sent, recieved in response:
            
            # PARSE RESPONSE FOR IP AND MAC
            ip_found = recieved.psrc
            mac_found = recieved.hwsrc
            
            # GET HOST AND VENDOR FROM EXTERNAL MODULE
            vendor = self.exe.get_vendor(mac_found)
            host = self.exe.get_host(ip_found)

            
            
            # CHECK IF DEVICE ALREADY HAS ITS OWN THREAD
            listed = any(ip_found == ip for ip in self.active_devices)
 

            if listed != True and ip_found:
                
                # APPEND THE ONLINE DEVICE TO A LIST
                self.active_devices.append(ip_found)

                # START A DEDICATED THREAD FOR THIS IP
                threading.Thread(target=self.sniffer.pinger, args=(ip_found, mac_found, vendor), daemon=True).start()  # FOR CONNECTION STATUS TRACKING
                threading.Thread(target=packet_capture().sniffer, args=(ip_found, mac_found, host, vendor), daemon=True).start()   # FOR PACKET CAPTURE // SAVING
                threading.Thread(target=Common_port_scan().scanner, args=(ip_found, mac_found, host, vendor), daemon=True).start()  # FOR COMMON PORT SCANNING
         
    
    def threader(self):
        """Responsible for creating a thread for each ip in the given subnet"""

        subnet = self.get_subnet()
        threads = []

        # STARTING MESSAGE
        say = f"Welcome to NetSniffer.I will be your assistant today. I was created by Bari, to breach and capture any and all network traffic.  I will Now perform a ARP scan on your network."
        #Utilities().tts(say)
        
        while True:

            for ip in subnet:

                #console.print(f"[bold blue]Scanning:[/bold blue][bold red] {ip}[/bold red]")
                t = threading.Thread(target=self.arp_scanner, args=(ip,))
                threads.append(t)
            
            for thread in threads:
                thread.start()
            
            for thread in threads:
                thread.join()
            console.print("[bold green]DONEEE[/bold green]")
            
            time.sleep(3)
            console.print(f"\n\nDone: {self.active_devices}")
            ip_logging().device_count(count=len(self.active_devices), devices=self.active_devices)
            
            
            while True:
              pass
                
        
if __name__ == "__main__":

    main = subnet_scanner()

    main.threader()
            



        
