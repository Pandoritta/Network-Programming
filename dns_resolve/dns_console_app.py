from dns import resolver
import argparse
import socket
import ipaddress
import sys


class DNSResolver:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="DNS Resolver")
        self.setup_parser()

    def setup_parser(self):
        self.parser.add_argument('--domain', help='Domain name to resolve')
        self.parser.add_argument('--ip', help='IP address to reverse lookup')
        self.parser.add_argument('--dns-server', help='Custom DNS server to use')

    def show_menu(self):
        while True:
            print("\n\033[32m >DNS Resolver Menu: \033[0m")
            print(" \033[32m >1. Resolve Domain Name \033[0m")
            print(" \033[32m >2. Resolve IP Address \033[0m")
            print(" \033[32m >3. Use Custom DNS Server \033[0m")
            print(" \033[32m >4. Exit \033[0m")
            

            choice = input("\n\033[95m Enter your choice (1-4): \033[0m")
            return choice



    def resolve_dns(self, domain_name):
        try:
            result = resolver.resolve(domain_name, 'A')
            for ipval in result:
                print(f"IP Address: {ipval.to_text()}")
        except resolver.NoAnswer:
            print("No answer from DNS server.")
        except resolver.NXDOMAIN:
            print("Domain does not exist.")
        except resolver.Timeout:
            print("DNS query timed out.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return result
    

    def resolve_ip(self, ip_address):
        try:
            data = socket.gethostbyaddr(ip_address)
            host = repr(data[0])
            print(f"Host name: {host}")         
            return host
        except Exception:
            return False
        
    def print_current_dns(self):

        resolve = resolver.get_default_resolver()   
        nameserver = resolve.nameservers               

        if not nameserver:
            print("No DNS servers configured.")
            return

        print("Current DNS server is:")
        for ns in nameserver:
            print(f"  • {ns}")

    def use_dns_server(self, dns_server):
        try:
            socket.inet_aton(dns_server)
            resolver.default_resolver.nameservers = [dns_server]
            print(f"Using custom DNS server: {dns_server}")
        except socket.error:
            print(f"Invalid DNS server IP address: {dns_server}")

    def validate_ip(self, ip_address) -> bool:
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            print(f"Invalid IP address: {ip_address}")
            return False
    
    def handle_choice(self, choice):
        if choice == '1':
            domain_name = input("Enter domain name: ")
            self.resolve_dns(domain_name)
        elif choice == '2':
            ip_address = input("Enter IP address: ")
            if self.validate_ip(ip_address):
                self.resolve_ip(ip_address)
        elif choice == '3':
            self.print_current_dns()
            dns_server = input("Enter custom DNS server IP: ")
            self.use_dns_server(dns_server)
        elif choice == '4':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    dns_resolver = DNSResolver()
    while True:
        choice = dns_resolver.show_menu()
        dns_resolver.handle_choice(choice)
