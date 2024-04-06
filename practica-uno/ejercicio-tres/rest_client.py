import requests
from urllib.parse import quote
url = "http://localhost:8000/pacientes"

# Crear otro nuevo paciente
nuevo_paciente = {
    "CI": "9876543",
    "Nombre": "Maria",
    "Apellido": "Lopez",
    "Edad": 28,
    "Genero": "Femenino",
    "Diagnostico": "Diabetes",
    "Doctor": "Dra. Martinez"
}

post_response = requests.request(method="POST", url=url, json=nuevo_paciente)
print("\nPOST /pacientes")
print(post_response.text)

# GET /pacientes
response = requests.get(url)
print("\nGET /pacientes")
print(response.json())

# GET /pacientes/ci=9876543
ci_paciente = "1234567"
url_ci_paciente = f"{url}/{ci_paciente}"
get_response = requests.request(method="GET", url=url_ci_paciente)
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


ci_paciente = "1234567"
url_ci_paciente = f"{url}/{ci_paciente}"
nuevo_paciente = {
    "CI": "1234567",
    "Nombre": "Juan",
    "Apellido": "Perez",
    "Edad": 36,
    "Genero": "Masculino",
    "Diagnostico": "Diabetes",
    "Doctor": "Dr. Garcia"
}
put_response = requests.request(method="PUT", url=url_ci_paciente, json=nuevo_paciente)
print(f"\nPUT /pacientes/{ci_paciente}")
print(put_response.text)

put_response = requests.request(method="DELETE", url=url_ci_paciente)
print(f"\nDELETE /pacientes/{ci_paciente}")
print(put_response.text)