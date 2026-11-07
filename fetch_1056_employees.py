import json
import requests
import re

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Origin': 'https://mapims-hrms.tecvinesolutions.com',
    'Referer': 'https://mapims-hrms.tecvinesolutions.com/login'
}

csrf_res = session.get('https://mapims-hrms.tecvinesolutions.com/api/auth/csrf', headers=headers)
csrf_token = csrf_res.json().get('csrfToken')

login_payload = {
    'csrfToken': csrf_token,
    'identifier': '7200504251',
    'password': 'Solai@123',
    'json': 'true',
    'redirect': 'false',
    'callbackUrl': 'https://mapims-hrms.tecvinesolutions.com/'
}
session.post('https://mapims-hrms.tecvinesolutions.com/api/auth/callback/credentials', data=login_payload, headers=headers)
session_res = session.get('https://mapims-hrms.tecvinesolutions.com/api/auth/session', headers=headers)
token = session_res.json()['user']['accessToken']

api_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

base_url = 'https://mapims-hrms-api.tecvinesolutions.com/api/v1'

print("[*] Fetching all 1056 employees from /employee/dropdown...")
r = session.get(f'{base_url}/employee/dropdown?includeInvitedUsers=true', headers=api_headers, timeout=15)
employees_raw = r.json()

print(f"[+] Total raw employees fetched: {len(employees_raw)}")

# Parse name and employee code
parsed_employees = []
for item in employees_raw:
    val = item.get('value', '').strip()
    key = item.get('key', '')
    disabled = item.get('disabled', False)
    
    # Extract code e.g. "Aameena M (40173)" -> name: "Aameena M", code: "40173"
    match = re.search(r'^(.*?)\s*\((\d+)\)$', val)
    if match:
        name = match.group(1).strip()
        code = match.group(2).strip()
    else:
        name = val
        code = ""
        
    parsed_employees.append({
        "recordId": key,
        "name": name,
        "code": code,
        "raw": val,
        "isInvited": disabled,
        "status": "Active" if not disabled else "Pending"
    })

print(f"[+] Successfully parsed {len(parsed_employees)} employees!")
print("Sample parsed items:")
for p in parsed_employees[:5]:
    print(" ", p)

# Save to json file
with open('all_1056_employees.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_employees, f, indent=2)

print("\nSaved all_1056_employees.json successfully!")

