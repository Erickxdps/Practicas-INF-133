import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los animales por la ruta /animales
ruta_get = url + "animales"

#POST
ruta_post = url + "animales"
nuevo_animal = {
        "nombre": "Willi",
        "especie": "Orangutan",
        "genero": "Masculino",
        "edad": 20,
        "peso": 80,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print("\nPOST /animales")
print(post_response.text)

#GET
get_response = requests.request(method="GET", url=ruta_get)
print("\nGET /animales")
print(get_response.text)

# GET /animales?especie=Mono
ruta_get = url + "animales?especie=Mono"
get_response = requests.request(method="GET", url=ruta_get)
print("\nGET /animales?especie=Mono")
print(get_response.text)

# GET /animales?especie=Mono
ruta_get = url + "animales?genero=Masculino"
get_response = requests.request(method="GET", url=ruta_get)
print("\nGET /animales?genero=Masculino")
print(get_response.text)

#PUT
nuevo_animal = {
        "nombre": "Willi",
        "especie": "Orangutan",
        "genero": "Masculino",
        "edad": 25,
        "peso": 70,
}
put_response = requests.request(method="PUT", url=ruta_post+"/1", json=nuevo_animal)
print("\nPUT/animales")
print(put_response.text)

#Delete
nuevo_animal = {
    "nombre": "Willi",
    "especie": "Orangutan",
    "genero": "Masculino",
    "edad": 20,
    "peso": 80,
}
delete_response = requests.request(method="DELETE", url=ruta_post+"/1", json=nuevo_animal)
print("\nDELETE /animales")
print(delete_response.text)





