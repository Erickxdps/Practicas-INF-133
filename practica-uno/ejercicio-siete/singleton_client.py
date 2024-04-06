import requests

url = "http://localhost:8000/partidas"

# POST /partidas
response = requests.request(
    method="POST", url=url, json={"elemento": "piedra"}
)
print("primera partida")
print(response.text)
response = requests.request(
    method="POST", url=url, json={"elemento": "piedra"}
)
print("\nsegunda partida")
print(response.text)
response = requests.request(
    method="POST", url=url, json={"elemento": "piedra"}
)
print("\ntercera partida")
print(response.text)

# GET /partidas
response = requests.request(method="GET", url=url)
print("\nGET /partidas")
print(response.text)

#GET /partidas?resultado={resultado}
url_resultado =url+ "?resultado=gano"
response = requests.request(method="GET", url=url_resultado)
print("\nGET /partidas?resultado=gano")
print(response.text)
