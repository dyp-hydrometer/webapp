import requests
import random
import datetime
from faker import Faker
from faker.providers import python
import json

fake = Faker()
now = datetime.datetime.utcnow()
headers = {'Content-type': 'application/json'}

for x in range(0, 100):
    data = {}
    data["temp"] = fake.pyfloat(min_value=75., max_value=79.)
    temp = fake.pyfloat(min_value=1, max_value=2)
    while temp > 1.050 and temp < 1.010:
        temp = float("{0:.3f}".format(fake.pyfloat(min_value=1, max_value=2)))
    data["specific_gravity"] = temp
    # add x * 5 seconds to the time of first execution
    b = now + datetime.timedelta(0,x*5)
    data["time"] = b.strftime("%Y-%m-%d %H:%M:%S")
    data["rssi"] = fake.pyint(min_value=-70, max_value=-30, step=1)
    print(data)
    resp = requests.put('http://localhost:5000/api/hydrometers/2/reading/', data=json.dumps(data), headers=headers)
    print(resp.status_code)