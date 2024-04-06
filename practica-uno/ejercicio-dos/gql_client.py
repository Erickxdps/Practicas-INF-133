import requests

url = 'http://localhost:8000/graphql'

# Crear una planta
mutation_crear_planta = """
mutation {
    crearPlanta(nombreComun: "Orquidea", especie: "Orchidaceae", edadMeses: 30, alturaCm: 150, frutos: true) {
        planta {
            id
            nombreComun
            especie
            edadMeses
            alturaCm
            frutos
        }
    }
}
"""

response = requests.post(url, json={'query': mutation_crear_planta})
print("Creando planta")
print(response.text)

# Listar todas las plantas
query_listar_plantas = """
{
    plantas {
        id
        nombreComun
        especie
        edadMeses
        alturaCm
        frutos
    }
}
"""

response = requests.post(url, json={'query': query_listar_plantas})
print("\nListar todas las plantas")
print(response.text)

# Buscar plantas por especie
query_buscar_por_especie = """
{
    plantasPorEspecie(especie: "Rosa") {
        nombreComun
        especie
    }
}
"""

response = requests.post(url, json={'query': query_buscar_por_especie})
print("\nBuscar plantas por especie")
print(response.text)

# Buscar las plantas que tienen frutos
query_plantas_con_frutos = """
{
    plantasConFrutos {
        nombreComun
        frutos
    }
}
"""

response = requests.post(url, json={'query': query_plantas_con_frutos})
print("\nBuscar las plantas que tienen frutos")
print(response.text)

# Actualizar la informacion de una planta (ID 1)
mutation_actualizar_planta = """
mutation {
    actualizarPlanta(id: 1, nombreComun: "Orquidea", especie: "Orchidaceae", edadMeses: 35, alturaCm: 160, frutos: true) {
        planta {
            nombreComun
        }
    }
}
"""

response = requests.post(url, json={'query': mutation_actualizar_planta})
print("\nActualizar la información de una planta")
print(response.text)

# Eliminar una planta
mutation_eliminar_planta = """
mutation {
    deletePlanta(id: 2) {
        planta {
            nombreComun
        }
    }
}
"""

response = requests.post(url, json={'query': mutation_eliminar_planta})
print("\nEliminar una planta")
print(response.text)

# Verificar que la planta ha sido eliminada
response = requests.post(url, json={'query': query_listar_plantas})
print("\nListar todas las plantas")
print(response.text)
