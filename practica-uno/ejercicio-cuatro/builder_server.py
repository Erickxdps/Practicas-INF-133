from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Producto: Paciente

pacientes={

}

class Paciente:
    def __init__(self):
        self.CI = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

    def set_ci(self, CI):
        self.CI = CI
        
    def __str__(self):
        return f"Nombre: {self.nombre},Apellido: {self.apellido},Edad: {self.edad},Genero: {self.genero},Diagnostico: {self.diagnostico},Doctor: {self.doctor}"


# Builder: Constructor de Pacientes
class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()

    def set_ci(self, CI):
        self.paciente.set_ci(CI)
        
    def set_nombre(self, nombre):
        self.paciente.nombre = nombre

    def set_apellido(self, apellido):
        self.paciente.apellido = apellido

    def set_edad(self, edad):
        self.paciente.edad = edad

    def set_genero(self, genero):
        self.paciente.genero = genero

    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico

    def set_doctor(self, doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente
    
    

# Director: Hospital
class Hospital:
    def __init__(self, builder):
        self.builder = builder

    def create_paciente(self, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        
        return self.builder.get_paciente()
    def read_pacientes(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}

    

# Aplicando el principio de responsabilidad única (S de SOLID)
class PacienteService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)

    def create_paciente(self, post_data):
        CI = post_data.get('CI', None)
        nombre = post_data.get('nombre', None)
        apellido = post_data.get('apellido', None)
        edad = post_data.get('edad', None)
        genero = post_data.get('genero', None)
        diagnostico = post_data.get('diagnostico', None)
        doctor = post_data.get('doctor', None)
        
        paciente = self.hospital.create_paciente(nombre,apellido,edad,genero,diagnostico,doctor)
        paciente.set_ci(CI)
        pacientes[CI] = paciente
        
        return paciente
    
    
    def read_pacientes(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}

    def update_paciente(self, index, post_data):
        if index in pacientes:
            paciente = pacientes[index]
            nombre = post_data.get('nombre', None)
            apellido = post_data.get('apellido', None)
            edad = post_data.get('edad', None)
            genero = post_data.get('genero', None)
            diagnostico = post_data.get('diagnostico', None)
            doctor = post_data.get('doctor', None)

            if nombre:
                paciente.nombre = nombre
            if apellido:
                paciente.apellido = apellido
            if edad:
                paciente.edad = edad
            if genero:
                paciente.genero = genero
            if diagnostico:
                paciente.diagnostico = diagnostico
            if doctor:
                paciente.doctor = doctor

            return paciente
        else:
            return None

    def delete_paciente(self, index):
        if index in pacientes:
            return pacientes.pop(index)
        else:
            return None
    #devuelve el paciente por su ci
    def get_paciente_by_ci(self, ci):
        for paciente in pacientes.values():
            if paciente.CI == ci:
                return paciente
        return None
    #devuelve el paciente por su diagnostico
    def get_paciente_by_diagnostico(self, diagnostico):
        for paciente in pacientes.values():
            if paciente.diagnostico == diagnostico:
                return paciente
        return None
    #devuelve el paciente por su doctor
    def get_paciente_by_doctor(self, doctor):
        for paciente in pacientes.values():
            if paciente.doctor == doctor:
                return paciente
        return None
    
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    
# Manejador de solicitudes HTTP
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PacienteService()
        super().__init__(*args, **kwargs)
    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_paciente(data)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        if self.path.startswith("/pacientes/"):
            ci_paciente = self.path.split("/")[2]
            paciente = self.controller.get_paciente_by_ci(ci_paciente)
            if paciente:
                HTTPDataHandler.handle_response(self, 200, paciente.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        elif "/pacientes" in self.path and "diagnostico=" in self.path:
            diagnostico = self.path.split("diagnostico=")[1].replace("%20", " ")
            pacientes_diagnostico = self.controller.get_paciente_by_diagnostico(diagnostico)
            if pacientes_diagnostico:
                HTTPDataHandler.handle_response(self, 200, pacientes_diagnostico.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "No se encontraron pacientes con el diagnóstico especificado"}
                )
        elif "/pacientes" in self.path and "doctor=" in self.path:
            doctor = self.path.split("doctor=")[1].replace("%20", " ")
            pacientes_doctor = self.controller.get_paciente_by_doctor(doctor)
            if pacientes_doctor:
                HTTPDataHandler.handle_response(self, 200, pacientes_doctor.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "No se encontraron pacientes con el diagnóstico especificado"}
                )
        elif self.path == "/pacientes":
            response_data = self.controller.read_pacientes()
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci_paciente = self.path.split("/")[2]
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(ci_paciente, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "CI de paciente no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci_paciente = self.path.split("/")[2]
            deleted_paciente = self.controller.delete_paciente(ci_paciente)
            if deleted_paciente:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Paciente eliminado correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
