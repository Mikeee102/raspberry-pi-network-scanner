import nmap
import socket

def scan_network(ip_range):
    """
    Run an Nmap scan on the given IP range using faster settings.
    """
    scanner = nmap.PortScanner()
    print(f"[INFO] Starting quick network scan for: {ip_range}")
    nm_arguments = "-sV --top-ports 1000 -T4 --version-intensity 5"
    scanner.scan(ip_range, arguments=nm_arguments)

    host_list = []
    for host in scanner.all_hosts():
        host_info = {
            'ip': host,
            'hostname': scanner[host].hostname(),
            'state': scanner[host].state(),
            'ports': []
        }

        # Check all protocols Nmap found
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            for port in ports:
                port_state = scanner[host][proto][port]['state']
                service_name = scanner[host][proto][port].get('name', 'unknown')
                service_version = scanner[host][proto][port].get('version', 'unknown')

                # If version is unknown and port is open, try banner grabbing
                if port_state == 'open' and service_version == 'unknown':
                    grabbed_version = banner_grab(host, port, service_name)
                    if grabbed_version:
                        service_version = grabbed_version

                port_info = {
                    'port': port,
                    'state': port_state,
                    'name': service_name,
                    'version': service_version
                }
                host_info['ports'].append(port_info)

        host_list.append(host_info)

    return host_list


def banner_grab(ip, port, service_name):
    """
    Try to grab more info if Nmap didn't detect a version.
    """
    try:
        # SSH banner
        if service_name == 'ssh' or port == 22:
            sock = socket.socket()
            sock.settimeout(2)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            if banner:
                return banner.strip()

        # HTTP/HTTPS banner
        elif service_name in ['http', 'ssl/http'] or port in [80, 8080, 443]:
            sock = socket.socket()
            sock.settimeout(2)
            sock.connect((ip, port))
            http_req = b"GET / HTTP/1.0\r\nHost: " + ip.encode() + b"\r\n\r\n"
            sock.send(http_req)
            response = sock.recv(2048).decode('utf-8', errors='ignore')
            sock.close()

            if response:
                # Look for 'Server:' header
                for line in response.split('\r\n'):
                    if line.lower().startswith('server:'):
                        server_line = line.split(':', 1)[1].strip()
                        return f"HTTP Banner: {server_line}"

                # If no 'Server:' header found, return a partial response
                resp_part = response[:50].replace('\n', ' ')
                return f"HTTP Response partial: {resp_part}"

        return None

    except Exception:
        # Connection error or timeout
        return None
