import requests

response = requests.get("https://idir.uta.edu/factchecker/score_text/{Hello this is a test.}")
temp = response.json()
print(response)
print(response.json())
print(temp['results'][0]['score'])

