import requests
import csv

url = 'http://127.0.0.1:8000/nodes'  # Replace with your API URL

response = requests.get(url)

file_path = "synonyms.csv"

out_data = []

if response.status_code == 200:
    data = response.json()
    nodes = data['nodes']

    for n in nodes:
        u1 = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/drugbank/{n}/JSON"
        r = requests.get(u1)

        if r.status_code == 200:
            r = r.json()

            if "PC_Substances" in r:
                synonyms = r["PC_Substances"][0]["synonyms"]
                print(n)
                l = list([n] + synonyms)
                out_data.append(l)


with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(out_data)
