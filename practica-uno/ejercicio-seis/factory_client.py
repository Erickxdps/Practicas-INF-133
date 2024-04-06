import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

# Consulta POST para crear un nuevo animal
new_animal_data = {
    "nombre": "León",
    "especie": "Felino",
    "genero": "Masculino",
    "edad": 5,
    "peso": 200
}
response = requests.post(url, data=json.dumps(new_animal_data), headers=headers)
new_animal_data = {
    "nombre": "Elefante",
    "especie": "Mamífero",
    "genero": "Femenino",
    "edad": 10,
    "peso": 5000
}
response = requests.post(url, data=json.dumps(new_animal_data), headers=headers)
print("\nPOST /animales")
print(response.json())

# Consulta GET para obtener todos los animales
response = requests.get(url)
print("\nGET /animales")
print(response.json())

# Consulta GET para obtener animales por especie
especie = "Felino"
response = requests.get(f"{url}?especie={especie}")
print("\nGET /animales?especie={especie}")
print(response.json())
print()

# Consulta GET para obtener animales por género
genero = "Masculino"
response = requests.get(f"{url}?genero={genero}")
print("\nGET /animales?genero={genero}")
print(response.json())
print()

# Consulta PUT para actualizar un animal por su ID
update_data = {
    "edad": 6,
    "peso": 220
}
response = requests.put(f"{url}/1", data=json.dumps(update_data), headers=headers)
print("\nPUT /animales/{ID}")
print(response.json())
print()

# Consulta DELETE para eliminar un animal por su ID
response = requests.delete(f"{url}/1")
print("\nDELETE /animales/{ID}")
print(response.json())
