import os
from scanner import scan_network
from vuln_checker import check_vulnerabilities
from brute_forcer import ssh_brute_force_async
from report_generator import generate_report

def get_password_list():
    """
    Keep asking for a valid, non-empty password file.
    """
    while True:
        password_file = input("Enter path to the password list (e.g. /home/pi/passwords.txt): ")
        if not os.path.isfile(password_file):
            print("[ERROR] File not found. Try again...")
            continue

        with open(password_file, 'r') as f:
            password_list = [p.strip() for p in f if p.strip()]

        if not password_list:
            print("[ERROR] File is empty. Try again...")
        else:
            return password_list

def main():
    # Step 1: define the network
    ip_range = "192.168.1.0/24"
    print(f"[INFO] Scanning the network: {ip_range}")

    # Step 2: run network scan
    scan_results = scan_network(ip_range)

    # Step 3: check for vulnerabilities
    vuln_report_data = []
    for host in scan_results:
        for port_info in host['ports']:
            service = port_info['name']
            version = port_info['version']

            found_vulns = check_vulnerabilities(service, version)
            if found_vulns:
                vuln_report_data.append({
                    'service': service,
                    'version': version,
                    'cve_list': found_vulns
                })

    # If no vulns found, use placeholder
    if not vuln_report_data:
        vuln_report_data.append({
            'service': 'N/A',
            'version': 'N/A',
            'cve_list': [
                {
                    'id': 'None',
                    'title': 'No vulnerabilities found or recognized',
                    'score': 'N/A'
                }
            ]
        })

    # Step 4: SSH brute force
    brute_report_data = []
    do_bruteforce = input("Run SSH brute force? (yes/no): ")
    if do_bruteforce.lower() == "yes":
        username = input("Enter SSH username: ")
        password_list = get_password_list()

        for host in scan_results:
            for port_info in host['ports']:
                if port_info['name'] == 'ssh' and port_info['state'] == 'open':
                    ip = host['ip']
                    found_password = ssh_brute_force_async(
                        hostname=ip,
                        port=port_info['port'],
                        username=username,
                        password_list=password_list,
                        concurrency_limit=10
                    )
                    brute_report_data.append({
                        'ip': ip,
                        'user': username,
                        'success': True if found_password else False,
                        'password': found_password
                    })

    # Step 5: generate report
    report_filename = "pentest_report.pdf"
    generate_report(scan_results, vuln_report_data, brute_report_data, report_filename)
    print("[INFO] Pentest done. Report created:", report_filename)

if __name__ == "__main__":
    main()
