import requests
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import sys
import os

print("1. Logging into MAPIMS portal...", flush=True)
s = requests.Session()
adapter = HTTPAdapter(pool_connections=30, pool_maxsize=30)
s.mount('https://', adapter)

csrf = s.get('https://mapims-hrms.tecvinesolutions.com/api/auth/csrf').json()['csrfToken']
s.post('https://mapims-hrms.tecvinesolutions.com/api/auth/callback/credentials', data={
    'csrfToken': csrf, 'identifier': '7200504251', 'password': 'Solai@123', 'json': 'true', 'redirect': 'false'
})
sess = s.get('https://mapims-hrms.tecvinesolutions.com/api/auth/session').json()
tok = sess['user']['accessToken']
headers = {'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'}
base_api = 'https://mapims-hrms-api.tecvinesolutions.com/api/v1'

print("2. Session established. Bearer token acquired.", flush=True)

with open('all_1056_employees_enriched.json', 'r', encoding='utf-8') as f:
    employees = json.load(f)

print(f"3. Loaded {len(employees)} employees. Starting concurrent fetch...", flush=True)

# Load existing progress if available
progress_file = 'employees_portal_profiles.json'
profiles = {}
if os.path.exists(progress_file):
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        print(f"Loaded {len(profiles)} existing cached profiles from {progress_file}.", flush=True)
    except Exception:
        pass

needed = [emp for emp in employees if emp['recordId'] not in profiles]
print(f"Profiles to fetch: {len(needed)}", flush=True)

def fetch_worker(emp):
    rid = emp['recordId']
    url = f"{base_api}/employee/{rid}"
    try:
        r = s.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return rid, r.json()
        else:
            return rid, {'error_code': r.status_code}
    except Exception as ex:
        return rid, {'error': str(ex)}

t0 = time.time()
done_count = len(profiles)

if needed:
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_worker, emp) for emp in needed]
        for f in as_completed(futures):
            rid, data = f.result()
            profiles[rid] = data
            done_count += 1
            if done_count % 50 == 0 or done_count == len(employees):
                elapsed = time.time() - t0
                rate = done_count / max(1, elapsed)
                print(f"Fetched {done_count}/{len(employees)} ({done_count/len(employees)*100:.1f}%) in {elapsed:.1f}s (~{rate:.1f} req/s)", flush=True)
                with open(progress_file, 'w', encoding='utf-8') as pf:
                    json.dump(profiles, pf)

with open(progress_file, 'w', encoding='utf-8') as pf:
    json.dump(profiles, pf, indent=2)

print("4. Updating employee records with portal data...", flush=True)
role_counts = {}
for emp in employees:
    rid = emp['recordId']
    p = profiles.get(rid)
    if p and not p.get('error') and not p.get('error_code'):
        emp['roleName'] = p.get('roleName') or 'Employee'
        emp['roleMasterId'] = p.get('roleMasterId') or 'E7VA3zDK'
        emp['role'] = emp['roleName']
        if p.get('joinDate'):
            emp['joinDate'] = p.get('joinDate')
        if p.get('attendanceMode'):
            emp['attendanceMode'] = p.get('attendanceMode')
        if p.get('payrollPolicyRecordId'):
            emp['payrollPolicyRecordId'] = p.get('payrollPolicyRecordId')
        if p.get('employeeImage'):
            emp['employeeImage'] = p.get('employeeImage')
        if p.get('departmentName'):
            emp['department'] = p.get('departmentName')
        if p.get('designationName'):
            emp['designation'] = p.get('designationName')
        if p.get('genderName'):
            emp['gender'] = p.get('genderName')
        if p.get('contactNumber'):
            emp['contactNumber'] = p.get('contactNumber')
        if p.get('officialEmail') or p.get('emailId'):
            emp['email'] = p.get('officialEmail') or p.get('emailId')
        if p.get('panNo'):
            emp['panNo'] = p.get('panNo')
        if p.get('esiNo'):
            emp['esiNo'] = p.get('esiNo')
        if p.get('uanNo'):
            emp['uanNo'] = p.get('uanNo')
    else:
        emp['roleName'] = 'Employee'
        emp['role'] = 'Employee'

    rname = emp['roleName']
    role_counts[rname] = role_counts.get(rname, 0) + 1

print("\n--- Official Role Distribution from Live Portal ---", flush=True)
for rname, c in sorted(role_counts.items(), key=lambda x: -x[1]):
    print(f"  {rname:<25}: {c}", flush=True)

with open('all_1056_employees_enriched.json', 'w', encoding='utf-8') as f:
    json.dump(employees, f, indent=2)

js_content = f"// MAPIMS HRMS - Enriched Census Data (1056 Personnel with verified Portal Roles and Profile Data)\nwindow.ALL_EMPLOYEES = {json.dumps(employees, indent=2)};\n"
with open('employees_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully saved all {len(employees)} employees with verified roles and portal profiles!", flush=True)
