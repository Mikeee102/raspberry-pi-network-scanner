import requests

VULNERS_API_URL = "https://vulners.com/api/v3/search/lucene/"

def check_vulnerabilities(service_name, version):
    """
    Check known vulnerabilities by service and version using the Vulners API.
    """
    query = f"{service_name} {version}"
    params = {
        'query': query,
        'size': 5
    }
    try:
        response = requests.get(VULNERS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        vulnerabilities = []
        documents = data.get('data', {}).get('documents', [])

        for doc in documents:
            vuln_id = doc.get('id')
            title = doc.get('title')
            score = doc.get('cvss', {}).get('score', 'Unknown')
            vulnerabilities.append({
                'id': vuln_id,
                'title': title,
                'score': score
            })

        return vulnerabilities

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Could not connect to Vulners API: {e}")
        return []
