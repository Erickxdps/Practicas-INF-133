import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from abc import ABC, abstractmethod

class Animal:
    def __init__(self, id, nombre, especie, genero, edad, peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "genero": self.genero,
            "edad": self.edad,
            "peso": self.peso
        }

class AnimalFactory(ABC):
    @abstractmethod
    def create_animal(self, nombre, especie, genero, edad, peso):
        pass

class MamiferoFactory(AnimalFactory):
    def create_animal(self, nombre, especie, genero, edad, peso):
        return Animal(nombre, especie, genero, edad, peso)

class Zoo:
    def __init__(self):
        self.animales = {}
        self.animal_id_counter = 0

    def create_animal(self, nombre, especie, genero, edad, peso):
        self.animal_id_counter += 1
        animal = Animal(self.animal_id_counter, nombre, especie, genero, edad, peso)
        self.animales[self.animal_id_counter] = animal
        return animal

    def get_animal(self, animal_id):
        return self.animales.get(animal_id)

    def get_all_animales(self):
        return [animal.to_dict() for animal in self.animales.values()]

    def get_animales_by_especie(self, especie):
        return [animal.to_dict() for animal in self.animales.values() if animal.especie == especie]

    def get_animales_by_genero(self, genero):
        return [animal.to_dict() for animal in self.animales.values() if animal.genero == genero]

    def update_animal(self, animal_id, nombre, especie, genero, edad, peso):
        if animal_id in self.animales:
            animal = self.animales[animal_id]
            animal.nombre = nombre
            animal.especie = especie
            animal.genero = genero
            animal.edad = edad
            animal.peso = peso
            return animal
        else:
            return None

    def delete_animal(self, animal_id):
        if animal_id in self.animales:
            del self.animales[animal_id]
            return True
        else:
            return False

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class ZooRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, zoo, *args, **kwargs):
        self.zoo = zoo
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            nombre = data.get("nombre")
            especie = data.get("especie")
            genero = data.get("genero")
            edad = data.get("edad")
            peso = data.get("peso")
            animal = self.zoo.create_animal(nombre, especie, genero, edad, peso)
            if animal:
                HTTPDataHandler.handle_response(self, 200, {"message": "Animal creado exitosamente", "animal": animal.to_dict()})
            else:
                HTTPDataHandler.handle_response(self, 400, {"message": "No se pudo crear el animal"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_GET(self):
        if self.path == "/animales":
            animales = self.zoo.get_all_animales()
            HTTPDataHandler.handle_response(self, 200, animales)
        elif "/animales?especie=" in self.path:
            especie = self.path.split("=")[-1]
            animales = self.zoo.get_animales_by_especie(especie)
            HTTPDataHandler.handle_response(self, 200, animales)
        elif "/animales?genero=" in self.path:
            genero = self.path.split("=")[-1]
            animales = self.zoo.get_animales_by_genero(genero)
            HTTPDataHandler.handle_response(self, 200, animales)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_PUT(self):
        if "/animales/" in self.path:
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            nombre = data.get("nombre")
            especie = data.get("especie")
            genero = data.get("genero")
            edad = data.get("edad")
            peso = data.get("peso")
            updated_animal = self.zoo.update_animal(animal_id, nombre, especie, genero, edad, peso)
            if updated_animal:
                HTTPDataHandler.handle_response(self, 200, {"message": "Animal actualizado exitosamente", "animal": updated_animal.to_dict()})
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_DELETE(self):
        if "/animales/" in self.path:
            animal_id = int(self.path.split("/")[-1])
            if self.zoo.delete_animal(animal_id):
                HTTPDataHandler.handle_response(self, 200, {"message": f"Animal con ID {animal_id} eliminado exitosamente"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"message": "Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})


def main():
    try:
        zoo = Zoo()
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, lambda *args, **kwargs: ZooRequestHandler(zoo, *args, **kwargs))
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
