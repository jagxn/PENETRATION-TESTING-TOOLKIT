import socket
import requests
from concurrent.futures import ThreadPoolExecutor

def display_banner():
    print("""
   ____  _____ _____ _   _ _______ ______ _____  
  |  _ \|  ___|_   _| \ | |__   __|  ____|  __ \ 
  | |_) | |__   | | |  \| |  | |  | |__  | |__) |
  |  ___|  __|  | | | . ` |  | |  |  __| |  ___/ 
  | |   | |_____| |_| |\  |  | |  | |____| |     
  |_|   |______|_____|_| \_|  |_|  |______|_|     
                                                  
  Simple Penetration Testing Tool
  """)

def port_scanner(target, ports):
    print(f"\n[+] Scanning {target}...")
    
    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((target, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port, 'tcp')
                    except:
                        service = "unknown"
                    print(f"[+] Port {port}/tcp open - {service}")
                    
                    # Try to grab banner
                    try:
                        s.settimeout(2)
                        banner = s.recv(1024).decode().strip()
                        if banner:
                            print(f"    Banner: {banner}")
                    except:
                        pass
        except:
            pass
    
    # Use threading for faster scanning
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scan_port, ports)
    
    print("\n[+] Port scan completed!")

def brute_force(url, username, passwords):
    print(f"\n[+] Starting brute force on {url}")
    print(f"[+] Target username: {username}")
    print(f"[+] Trying {len(passwords)} passwords...\n")
    
    for password in passwords:
        try:
            data = {
                'username': username,
                'password': password.strip()
            }
            response = requests.post(url, data=data)
            
            # Simple check for successful login (adjust based on target)
            if "login failed" not in response.text.lower():
                print(f"\n[+] SUCCESS! Credentials: {username}:{password}")
                return True
            print(f"Trying: {password.ljust(15)} => Failed", end='\r')
        except Exception as e:
            print(f"\nError: {e}")
            continue
    
    print("\n[-] Brute force completed. No valid credentials found.")
    return False

def main():
    display_banner()
    
    # Port scanning section
    print("\n" + "="*50)
    target = input("[?] Enter target IP or hostname: ").strip()
    port_range = input("[?] Enter port range (e.g., 1-100 or 80,443): ").strip()
    
    # Parse port range
    if '-' in port_range:
        start, end = map(int, port_range.split('-'))
        ports = range(start, end+1)
    elif ',' in port_range:
        ports = [int(p) for p in port_range.split(',')]
    else:
        ports = [int(port_range)]
    
    port_scanner(target, ports)
    
    # Brute force section
    print("\n" + "="*50)
    choice = input("\n[?] Do you want to perform brute force attack? (y/n): ").lower()
    if choice == 'y':
        url = input("[?] Enter login URL (e.g., http://site.com/login): ").strip()
        username = input("[?] Enter username to test: ").strip()
        
        # Password options
        print("\nPassword options:")
        print("1. Use built-in common passwords")
        print("2. Enter custom passwords (comma separated)")
        print("3. Load from file")
        option = input("[?] Choose option (1-3): ").strip()
        
        if option == '1':
            passwords = [
                'admin', 'password', '123456', '12345678', '1234',
                'qwerty', '12345', 'dragon', 'baseball', 'football',
                'letmein', 'monkey', 'shadow', 'sunshine', 'password1'
            ]
        elif option == '2':
            custom = input("[?] Enter passwords (comma separated): ").strip()
            passwords = [p.strip() for p in custom.split(',')]
        elif option == '3':
            file = input("[?] Enter password file path: ").strip()
            try:
                with open(file, 'r') as f:
                    passwords = [line.strip() for line in f]
            except:
                print("[-] Error reading file. Using default passwords.")
                passwords = ['admin', 'password', '123456']
        else:
            print("[-] Invalid option. Using default passwords.")
            passwords = ['admin', 'password', '123456']
        
        brute_force(url, username, passwords)
    
    print("\n[+] Testing completed. Remember to use this tool ethically!")

if __name__ == "__main__":
    main()