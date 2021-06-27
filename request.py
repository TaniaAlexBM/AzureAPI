import requests

BASE_ENDPOINT = 'http://127.0.0.1:5000/'

data = [{"nombre":"oscar","formato":"jpg","size":10},
{"nombre":"juan","formato":"png","size":17},
{"nombre":"pedro","formato":"jpeg","size":14}]

for i in range(len(data)):
    response = requests.post(BASE_ENDPOINT + 'Storage/' + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE_ENDPOINT + 'Storage/2')
print(response.json())