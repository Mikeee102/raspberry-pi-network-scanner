from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

def generate_report(scan_data, vuln_data, brute_data, filename="report.pdf"):
    """
    Creates a PDF report about hosts, vulnerabilities, and brute-force results.
    """
    c = canvas.Canvas(filename, pagesize=A4)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Automated Network Pentest Report")
    c.setFont("Helvetica", 12)

    # Date/Time
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    c.drawString(50, 780, f"Created on: {now}")

    y = 760

    # 1. Network scan results
    c.drawString(50, y, "=== Network Scan Results ===")
    y -= 20
    for host in scan_data:
        host_line = f"Host: {host['ip']} ({host['hostname']}), Status: {host['state']}"
        c.drawString(60, y, host_line)
        y -= 15
        for port_info in host['ports']:
            port_line = f"  - Port {port_info['port']}/{port_info['name']}, State: {port_info['state']}, Version: {port_info['version']}"
            c.drawString(70, y, port_line)
            y -= 15
        y -= 5

    # 2. Vulnerability analysis
    c.drawString(50, y, "=== Vulnerability Analysis ===")
    y -= 20
    for vuln in vuln_data:
        vuln_line = f"Service: {vuln['service']} v{vuln['version']} - Found CVEs:"
        c.drawString(60, y, vuln_line)
        y -= 15
        for cve in vuln['cve_list']:
            cve_line = f"  - {cve['id']}: {cve['title']} (CVSS: {cve['score']})"
            c.drawString(70, y, cve_line)
            y -= 15
        y -= 5

    # 3. Brute-force results
    c.drawString(50, y, "=== Brute-force Results ===")
    y -= 20
    for brute_res in brute_data:
        res_line = (f"Host: {brute_res['ip']}, User: {brute_res['user']}, "
                    f"Success: {brute_res['success']}, Password: {brute_res.get('password', 'N/A')}")
        c.drawString(60, y, res_line)
        y -= 15

    c.save()
    print(f"[INFO] Report saved as {filename}")
