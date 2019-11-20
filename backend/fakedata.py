import requests
import random
import datetime
from faker import Faker
from faker.providers import python
import json

fake = Faker()
now = datetime.datetime.utcnow()
headers = {'Content-type': 'application/json'}

for x in range(0,6):
    profile = {}
    profile["name"] = f"profile #{x}"
    profile["description"] = f"{x}"
    profile["req_temp"] = fake.pyfloat(min_value=75., max_value=79.)
    temp = fake.pyfloat(min_value=1, max_value=2)
    while temp > 1.050 and temp < 1.010:
        temp = float("{0:.3f}".format(fake.pyfloat(min_value=1, max_value=2)))
    profile["req_gravity"] = temp
    profile["duration"] = str(datetime.timedelta(days=14))
    resp = requests.post(f"http://localhost:5000/api/profiles/", data=json.dumps(profile), headers=headers)
    #resp = requests.get('http://localhost:5000/api/hydrometers/'+x, headers=headers)
    #if resp.status_code == 201:
    '''for y in range(0, 20):
        data = {}
        data["temp"] = fake.pyfloat(min_value=75., max_value=79.)
        temp = fake.pyfloat(min_value=1, max_value=2)
        while temp > 1.050 and temp < 1.010:
            temp = float("{0:.3f}".format(fake.pyfloat(min_value=1, max_value=2)))
        data["specific_gravity"] = temp
        # add x * 5 seconds to the time of first execution
        b = now + datetime.timedelta(0,y*5)
        data["time"] = b.strftime("%Y-%m-%d %H:%M:%S")
        print(data)
        resp = requests.put(f'http://localhost:5000/api/hydrometers/{x}/reading/', data=json.dumps(data), headers=headers)
        print(resp.status_code)'''