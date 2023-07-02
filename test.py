import requests

url = 'http://127.0.0.1:8000/nodes'  # Replace with your API URL

# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     nodes = data['nodes']
#     print('Nodes:', nodes)
# else:
#     print('Error:', response.status_code)


data = {'Name': "DB00382"}

response = requests.post(url, json=data)

if response.status_code == 201:
    neighbors = response.json()['neighbors']
    print('Neighbors:', neighbors)
else:
    print('Error:', response.text)
