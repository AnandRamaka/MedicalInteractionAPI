import requests

routes = ['/valid', '/neighbors', '/nodes']

print()
answer = input("Which operation? \n\n Choices:\n [1] Validate \n [2] Get nodes \n [3] Find neighbors\n\n")
choices = ["Validate", "Get nodes", "Find neighbors"]

while not answer.isdigit() or int(answer) < 1 or int(answer) > len(choices):
    print("\nInvalid input\n")
    answer = input("Which operation? \n\n Choices:\n [1] Validate \n [2] Get nodes \n [3] Find neighbors\n\n")


choice = choices[int(answer) - 1]
url = f'http://127.0.0.1:8000/{routes[int(answer) - 1]}'  

if choice == "Get Nodes":
    response = requests.get(url)
    print(response)
else:
    data = None
    if choice == "Validate":
        names = input("Enter a list of drugs seperated by a space...\n").split(" ")
        data = {"Names": names}
    else:
        name = input("Enter a drug name...\n")
        data = {"Name": name}

    response = requests.post(url, json=data)
    if response.status_code != 201:
        print("An error occured.")
    print(response.json())