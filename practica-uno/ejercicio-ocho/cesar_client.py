import requests
from urllib.parse import quote

url = "http://localhost:8000/mensajes"

# POST /mensajes
data = {
    "Contenido": "Hola Javis"
    }
response = requests.post(url, json=data)
print("POST /mensajes:", response.status_code)
print(response.json())

# GET /mensajes
response = requests.get(url)
print("\nGET /mensajes:", response.status_code)
print(response.json())

# GET /mensaje/ID
mensaje_id = response.json()[0]["ID"]
url_id = f"{url}/{mensaje_id}"
response = requests.get(url_id)
print("\nGET /mensajes/{ID}:")
print(response.json())

# PUT /mensaje/ID
updated_data = {
    "Contenido": "Comprate manos Javis"
    }
response = requests.put(url_id, json=updated_data)
print("\nPUT /mensajes/{ID}:")
print(response.json())

# DELETE/mensajes/ID
response = requests.delete(url_id)
print("\nDELETE /mensajes/{ID}:")
print(response.json())