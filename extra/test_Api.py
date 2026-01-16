import requests

url = "http://127.0.0.1:1112/profile"
data = {
	"email" : "ali@gmail.com",
    "password" : "11225588"
}
header = {
    'x-access-token' : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOSIsImV4cCI6MTc2ODM5Mzc5M30.Rv4mMXtPafHzcoLCqwwoFIVbcgLFjQ3SUsvfPQP89L0"
}
print("sending")
# response = requests.get(url, json=data, headers=header)
# print("sent")
# print("Status code:", response.status_code)
# print("Response body:", response.text)

import datetime

t1 = (datetime.date.today() + datetime.timedelta(days=1))
t2 = t1 + datetime.timedelta(days=1)
print(t2)
