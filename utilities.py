# UTILITIES MODULE FOR // MAIN MODULE


# IMPORTS
import pyttsx3, socket, manuf, requests

# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
console = Console()

class Utilities():
    """Utilities module to be imported in other modules for better modularity"""

    def __init__(self):
        pass

    def tts(self, say, voice_id = 0, rate_speed = 15):
        """Use this method to say thing through computer speakers"""

        # CREATE A OBJECT FOR TTS
        engine = pyttsx3.init()

        # SET VARIABLES
        try:
            voices = engine.getProperty('voices')
            rate = engine.getProperty('rate')
        except Exception as e:
            console.print(e)
            
            
        # SET PROPERTY VARIABLES

        
        # VOICE TO USE
        try:
            if len(voices) > 0:
                engine.setProperty('voice', voices[voice_id].id)
            else:
                engine.setProperty('voice', voices[voice_id].id)
        
        except Exception as e:
            console.print(f"{e}: Defaulting to voice_id of 0")
            engine.setProperty("voice", voices[0].id)
        

        # RATE TO SET SPEED
        try:
            engine.setProperty('rate', rate - rate_speed)
        
        except Exception as e:
            console.print(f"{e}: Defaulting to rate of 15")
            engine.setProperty('rate', rate -15)
        
        
        # NOW TO OUTPUT THAT VOICE
        engine.say(say)
        engine.runAndWait()
        
    
    def get_host(self, ip):
        """Responsible for finding the device host name"""

        try:
            host = socket.gethostbyaddr(ip)[0].split('.')[0]
        
        except Exception as e:
            host = "N/A"
        
        # RETURN HOST 
        finally:
            return host
    
    def get_vendor(self, mac):
        """Responsible for finding the device vendor"""
        
        # URL
        url = f"https://api.macvendors.com/{mac}"

        headers = {
            "bearer": "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImp0aSI6IjNlM2JiMTMzLWVmODItNGU1MC1iNDczLWRjMTY3ZTVjMmI3MyJ9.eyJpc3MiOiJtYWN2ZW5kb3JzIiwiYXVkIjoibWFjdmVuZG9ycyIsImp0aSI6IjNlM2JiMTMzLWVmODItNGU1MC1iNDczLWRjMTY3ZTVjMmI3MyIsImlhdCI6MTc0MTI0MzA0OSwiZXhwIjoyMDU1NzM5MDQ5LCJzdWIiOiIxNTY3OSIsInR5cCI6ImFjY2VzcyJ9.Y8BkLcz4fr1wCcKohdWGSmjoeIoxOo_wktdHO0iwt_pDEKq3VIDlcupeOnRLZnDnxxzt9pEGphIR47SV9S7x7w"
            }

        try:
            response = requests.get(url, timeout=2)

            if response.status_code == 200:
                vendor =  response.text
            
            else:
                vendor = manuf.MacParser().get_manuf_long(mac)

                vendor = vendor if vendor else "N/A"


        except Exception as e:
            vendor = manuf.MacParser().get_manuf_long(mac)

            vendor = vendor if vendor else "N/A"

        # RETURN VENDOR
        finally:
            return vendor
    
    
    # THEORETICAL FOR THE MOMENT
    def get_time(self, seconds):
        """Will be responsible for taking x amount of seconds and returning it in a xx:xx format"""

        if seconds > 60:
            seconds = f"{seconds}"
            time = int(seconds) / 60
            time_format = f"{time:.2f} : {seconds}"
            
            return time_format
         
        else:
            return seconds
    

    def get_name(self, vendor: str, host: str, ip: str):
        """This method will be used to help choose what the tts method will use to announce the device"""
        """For Example, If the device has a vendor name we will use that if not then host and if neither of those are availavle we will use the ip"""

        
        try:
            if vendor == "N/A" and host == "N/A":
                announce = ip

            elif host != "N/A":
                announce = host                
            
            elif vendor != "N/A":
                announce = vendor

                
        
        except Exception as e:
            console.print(e)
            announce = ip
        
        finally:
            return announce
        
        
