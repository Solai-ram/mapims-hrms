"""
HRMS Data Sync Script for Solairam P (60493)
Fetches live data from https://mapims-hrms.tecvinesolutions.com and updates solairam_hrms_data.json
"""

import sys
import json
import requests

def sync_hrms(phone="7200504251", password="Solai@123"):
    print(f"[*] Authenticating with HRMS portal for {phone}...")
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Origin': 'https://mapims-hrms.tecvinesolutions.com',
        'Referer': 'https://mapims-hrms.tecvinesolutions.com/login'
    }

    # 1. Fetch NextAuth CSRF token
    csrf_res = session.get('https://mapims-hrms.tecvinesolutions.com/api/auth/csrf', headers=headers)
    if csrf_res.status_code != 200:
        raise Exception(f"Failed to get CSRF token: {csrf_res.status_code}")
    csrf_token = csrf_res.json().get('csrfToken')

    # 2. Authenticate
    login_url = 'https://mapims-hrms.tecvinesolutions.com/api/auth/callback/credentials'
    payload = {
        'csrfToken': csrf_token,
        'identifier': phone,
        'password': password,
        'json': 'true',
        'redirect': 'false',
        'callbackUrl': 'https://mapims-hrms.tecvinesolutions.com/'
    }
    login_res = session.post(login_url, data=payload, headers=headers, allow_redirects=False)
    if login_res.status_code != 200:
        raise Exception(f"Login failed: {login_res.status_code} {login_res.text}")

    # 3. Retrieve Session & Token
    session_res = session.get('https://mapims-hrms.tecvinesolutions.com/api/auth/session', headers=headers)
    session_data = session_res.json()
    if not session_data.get('user'):
        raise Exception(f"Invalid session: {session_res.text}")

    access_token = session_data['user']['accessToken']
    print("[+] Successfully authenticated! Obtained Bearer token.")

    api_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'User-Agent': headers['User-Agent']
    }
    base_url = 'https://mapims-hrms-api.tecvinesolutions.com/api/v1'

    # 4. Fetch me
    print("[*] Fetching user identity and permissions (/me)...")
    me = session.get(f'{base_url}/me', headers=api_headers).json()
    emp_id = me.get('employeeId', '4Ygb6RgE')

    # 5. Fetch employee profile
    print(f"[*] Fetching employee profile for {emp_id}...")
    profile = session.get(f'{base_url}/employee/{emp_id}', headers=api_headers).json()

    # 6. Fetch dashboard stats
    print("[*] Fetching employee dashboard overview...")
    dashboard = session.get(f'{base_url}/employeeDashboard', headers=api_headers).json()

    # 7. Fetch attendance records
    print("[*] Fetching attendance details and biometric punches...")
    attendance = session.get(f'{base_url}/employeeDashboard/attendanceDetails', headers=api_headers).json()

    # 8. Fetch leave balances
    print("[*] Fetching leave balances...")
    leave_balance = session.get(f'{base_url}/employeeDashboard/leaveBalance', headers=api_headers).json()

    # 9. Fetch finance & payroll history
    print("[*] Fetching finance details...")
    finance = session.get(f'{base_url}/employeeDashboard/financeDetails', headers=api_headers).json()

    # 10. Fetch shifts & departments
    shifts = session.get(f'{base_url}/shift/dropdown', headers=api_headers).json()
    departments = session.get(f'{base_url}/department/dropdown', headers=api_headers).json()
    designations = session.get(f'{base_url}/designation/dropdown', headers=api_headers).json()

    # Save photo if available
    img_url = profile.get('employeeImage')
    if img_url:
        try:
            img_res = requests.get(img_url, timeout=10)
            if img_res.status_code == 200:
                with open('profile_photo.png', 'wb') as img_f:
                    img_f.write(img_res.content)
                print("[+] Saved updated profile_photo.png")
        except Exception as e:
            print(f"[!] Warning saving image: {e}")

    aggregated = {
        "sync_timestamp": session_res.headers.get('Date', ''),
        "me": me,
        "profile": profile,
        "dashboard": dashboard,
        "attendance": attendance,
        "leave_balances": leave_balance,
        "finance": finance,
        "shifts": shifts,
        "departments": departments,
        "designations": designations
    }

    with open('solairam_hrms_data.json', 'w', encoding='utf-8') as f:
        json.dump(aggregated, f, indent=2)

    print("[SUCCESS] All HRMS data refreshed and saved to solairam_hrms_data.json!")
    return aggregated

if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else "7200504251"
    pw = sys.argv[2] if len(sys.argv) > 2 else "Solai@123"
    sync_hrms(p, pw)

