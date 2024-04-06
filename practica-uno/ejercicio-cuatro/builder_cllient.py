import requests
from urllib.parse import quote
url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}

mi_paciente = {
    "CI": "1234567",
    "nombre": "Juan",
    "apellido": "Perez",
    "edad": 35,
    "genero": "Masculino",
    "diagnostico": "Hipertension",
    "doctor": "Pedro Perez"
}
response = requests.post(url, json=mi_paciente, headers=headers)
print("\nPOST/paciente")
print(response.json())


mi_paciente = {
    "CI" : "9876543",
    "nombre": "Maria",
    "apellido": "Lopez",
    "edad": 28,
    "genero": "Femenino",
    "diagnostico": "Diabetes",
    "doctor": "Dra. Martinez"
}
response = requests.post(url, json=mi_paciente, headers=headers)
print("\nPOST/paciente")
print(response.json())


response = requests.get(url, headers=headers)
print("\nGET/paciente")
print(response.json())

# GET /pacientes/ci
ci_paciente = "1234567"
url_ci_paciente = f"{url}/{ci_paciente}"
get_response = requests.get(url_ci_paciente, headers=headers)
print("\nGET /pacientes/{ci}")
print(get_response.text)


# GET /pacientes/?diagnostico=Diabetes
ruta_get = url + "?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print("\nGET /pacientes/?diagnostico=Diabetes")
print(get_response.text)

# GET /pacientes/?doctor=Pedro Perez
nombre_doctor = "Pedro Perez"
ruta_get = url + "?doctor=" + quote(nombre_doctor)
get_response = requests.request(method="GET", url=ruta_get)
print("\nGET /pacientes/?doctor=Pedro Perez")
print(get_response.text)





# PUT /pacientes/{ci}
edit_paciente = {
    "CI": "1234567",
    "nombre": "Juan",
    "apellido": "Perez",
    "edad": 36,
    "genero": "Masculino",
    "diagnostico": "Diabetes",
    "doctor": "Dr. Garcia"
}
url_edit_paciente = f"{url}/{edit_paciente['CI']}"
response = requests.put(url_edit_paciente, json=edit_paciente, headers=headers)
print(f"\nPUT /pacientes/{edit_paciente['CI']}")
print(response.json())

# DELETE /pacientes/{ci}
ci_paciente = "1234567" 
url_delete_paciente = f"{url}/{ci_paciente}"
response = requests.delete(url_delete_paciente)
print(f"\nDELETE /pacientes/{ci_paciente}")
print(response.json())
