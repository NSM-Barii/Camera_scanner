NetSniffer

WARNING - Be wary that this program utilizes a large amount of threads, Please make sure your machine has enough resources to effectively use the programs full capabilities 

NetSniffer is a powerful network monitoring tool designed to provide real-time data tracking, session management, and port scanning capabilities. Built as a red team counterpart to NetAlert, this tool is designed for cybersecurity professionals seeking to analyze network activity and identify potential vulnerabilities.

Features

🔹 Multi-threaded Scanning: Efficiently scans your network with dedicated threads for each IP address.
🔹 Data Tracking: Each IP has its own .txt file logging the data being sent, allowing for detailed packet analysis.
🔹 Connection Status Monitoring: Tracks device connectivity, session duration, and records uptime in real-time.
🔹 Port Scanning: Performs targeted port scans on each IP, with results stored in individual log files.
🔹 Stealth & Efficiency: Designed with performance and evasion techniques in mind for red team engagements.

How It Works

Network Scan: The program identifies all active IP addresses on the network.

Data Logging: Each identified IP gets a dedicated log file that tracks its data activity.

Session Tracking: A separate thread pings each IP to record its connection status and session duration.

Port Analysis: Another thread performs a comprehensive port scan and saves the results in individual text files.
