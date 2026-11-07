import json
import requests

with open('all_1056_employees_enriched.json', encoding='utf-8') as f:
    emps = json.load(f)

with_img = [e for e in emps if e.get('employeeImage')]
print(f"Total employees with employeeImage: {len(with_img)}")

for e in with_img[:5]:
    url = e['employeeImage']
    try:
        r = requests.get(url, timeout=10)
        print(f"Emp #{e.get('code')} photo fetch status: {r.status_code}, content-type: {r.headers.get('content-type')}, size: {len(r.content)} bytes")
    except Exception as ex:
        print(f"Emp #{e.get('code')} error: {ex}")
