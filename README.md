# Hack & Pi: Automated Pentesting with Raspberry Pi and Python

This repository provides a **portable, automated pentesting solution** that runs on a **Raspberry Pi** (or any Linux system). It combines **Nmap** for network scanning, **Vulners API** for vulnerability checks, an **asynchronous SSH bruteforce** module, and **PDF report generation** in a single workflow.

Repository: [https://github.com/Mikeee102/raspberry-pi-network-scanner](https://github.com/Mikeee102/raspberry-pi-network-scanner)

---

## Table of Contents

1. [Features](#features)  
2. [Requirements](#requirements)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Project Structure](#project-structure)  
6. [Configuration](#configuration)  
7. [Disclaimer](#disclaimer)  
8. [Further Ideas](#further-ideas)

---

## Features

- **Network Scanning**: Identifies hosts, open ports, and basic service/version information using [Nmap](https://nmap.org/).  
- **Vulnerability Checking**: Leverages the [Vulners API](https://vulners.com/) to match detected services against known CVEs.  
- **Asynchronous SSH Bruteforce**: Uses [asyncssh](https://asyncssh.readthedocs.io) for parallel password attempts on any open SSH ports found.  
- **PDF Reporting**: Generates a concise PDF file (`pentest_report.pdf`) detailing hosts, ports, vulnerabilities, and successful SSH brute force attempts.  
- **Portability**: Can run on a Raspberry Pi, making it easy to transport and quickly plug into different networks.

---

## Requirements

### Hardware

- **Raspberry Pi** (recommended: Pi 4 with at least 2 GB RAM)  
  - Alternatively, you can run this on any Linux machine. The Pi setup is just more convenient for portability.

### Software

- **Python 3** (version 3.6+)  
- **Git** (for cloning this repository)  
- **Nmap** (e.g., `sudo apt-get install nmap`)  
- **pip** (usually installed by default with Python 3)  
- *(Optional)* **libffi-dev** and **libssl-dev** on Debian/Ubuntu for compiling `asyncssh`.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mikeee102/raspberry-pi-network-scanner.git
   cd raspberry-pi-network-scanner
   ```

2. **Update your system** (recommended):
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

3. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip3 install python-nmap requests reportlab asyncssh termcolor
   ```

4. **(Optional) Create a virtual environment**:
   ```bash
   python3 -m venv pentest_env
   source pentest_env/bin/activate
   pip3 install -r requirements.txt
   ```

---

## Usage

1. **Connect Raspberry Pi to the target network**  
   - Ethernet or Wi-Fi is supported.  
   - Make sure you have **permission** to perform pentesting on that network.

2. **Run the main script**:
   ```bash
   python3 main.py
   ```
   - The script will ask if you want to perform an SSH bruteforce.  
   - If yes, you’ll be prompted for a username and the path to your password list.

3. **Wait for the scan and checks**  
   - The tool runs a network scan via Nmap, checks each detected service against the Vulners API, and optionally performs SSH password brute-forcing.

4. **View the PDF report**  
   - A file named `pentest_report.pdf` will appear in the project directory.  
   - Open it to see discovered hosts, open ports, found CVEs, and any successful brute-forced SSH credentials.

---

## Project Structure

A typical structure in this repository might look like this:

```plaintext
.
├── main.py
├── scanner.py
├── vuln_checker.py
├── brute_forcer.py
├── report_generator.py
├── requirements.txt
└── README.md
```

- **main.py**  
  Orchestrates scanning, vulnerability checks, optional SSH bruteforce, and PDF reporting.  
- **scanner.py**  
  Handles Nmap-based network scanning and optional banner grabbing for unknown services.  
- **vuln_checker.py**  
  Uses the Vulners API to fetch CVE details for identified services/versions.  
- **brute_forcer.py**  
  Provides an async SSH bruteforce module using [asyncssh](https://asyncssh.readthedocs.io).  
- **report_generator.py**  
  Generates a PDF report (via [ReportLab](https://www.reportlab.com/)) summarizing findings.

---

## Configuration

- **Network Range**:  
  By default, `ip_range` might be set to `"192.168.1.0/24"` in `main.py`. Adjust it to your local subnet or a specific target.

- **Nmap Arguments**:  
  In `scanner.py`, you can tweak the parameters (e.g., `-sV --top-ports 1000 -T4 --version-intensity 5`) to run more or less aggressive scans.

- **Vulners API**:  
  If you need an API key or want to handle rate limits, add logic in `vuln_checker.py`.

- **SSH Bruteforce**:  
  The user is prompted for a password list file. If no valid file is provided, the script will keep asking until a non-empty file is given.

---

## Disclaimer

This software is intended **exclusively** for legal security testing and educational purposes.

- **Do not** use it to attack systems or networks without **explicit written consent** from the owners.  
- Unauthorized scanning, brute forcing, or exploitation can be **illegal** and may lead to severe legal consequences.  
- The contributors assume **no liability** for misuse or damage caused by this tool.

---

## Further Ideas

- **Auto-Discovery**:  
  Implement a function that detects the local subnet automatically to avoid manually setting `ip_range`.

- **Web Interface**:  
  Wrap `main.py` in a simple Flask or Django web app to run scans and show results in a browser.

- **Custom Scripts**:  
  Extend `scanner.py` with additional Nmap NSE scripts for deeper vulnerability detection.

- **Additional Protocols**:  
  Add bruteforce checks for FTP, Telnet, SNMP, or HTTP forms.
