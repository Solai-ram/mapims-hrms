import requests

s = requests.Session()
csrf = s.get('https://mapims-hrms.tecvinesolutions.com/api/auth/csrf').json()['csrfToken']
s.post('https://mapims-hrms.tecvinesolutions.com/api/auth/callback/credentials', data={
    'csrfToken': csrf, 'identifier': '7200504251', 'password': 'Solai@123', 'json': 'true', 'redirect': 'false'
})
sess = s.get('https://mapims-hrms.tecvinesolutions.com/api/auth/session').json()
tok = sess['user']['accessToken']
headers = {'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'}
base_api = 'https://mapims-hrms-api.tecvinesolutions.com/api/v1'

# Test with 3 employees: Solairam P (4Ygb6RgE), Aameena M (BjgRAYVZ), Cathrine Lavenya (AGzE74VL)
test_rids = [
    ('4Ygb6RgE', '60493'),
    ('BjgRAYVZ', '40173'),
    ('AGzE74VL', '60191')
]

for rid, code in test_rids:
    r = s.get(f'{base_api}/employee/{rid}', headers=headers)
    if r.status_code == 200:
        emp_data = r.json()
        img_url = emp_data.get('employeeImage')
        print(f"\nEmp #{code} fresh img_url:")
        print(f"  {img_url[:90]}...")
        if img_url:
            r_img = requests.get(img_url, timeout=10)
            print(f"  Download status: {r_img.status_code}, length: {len(r_img.content)} bytes, Content-Type: {r_img.headers.get('content-type')}")
            if r_img.status_code == 200:
                with open(f"test_photo_{code}.png", "wb") as pf:
                    pf.write(r_img.content)
                print(f"  Successfully saved test_photo_{code}.png!")
    else:
        print(f"Emp #{code} profile fetch failed: {r.status_code}")
