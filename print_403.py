import json
import requests

with open('all_1056_employees_enriched.json', encoding='utf-8') as f:
    emps = json.load(f)

e = next(e for e in emps if e.get('employeeImage'))
r = requests.get(e['employeeImage'])
print("Status:", r.status_code)
print("Content:", r.text)
