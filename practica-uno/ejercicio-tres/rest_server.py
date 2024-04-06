from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Manejo de parámetros de consulta "query parameters" en la URL
from urllib.parse import urlparse, parse_qs

# Lista para almacenar la información de los pacientes
pacientes = [
    {
    "CI": "1234567",
    "Nombre": "Juan",
    "Apellido": "Perez",
    "Edad": 35,
    "Genero": "Masculino",
    "Diagnostico": "Hipertension",
    "Doctor": "Pedro Perez"
}
    ]


class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def find_patient(self, ci):
        return next(
            (paciente for paciente in pacientes if paciente["CI"] == ci),
            None,
        )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "ci" in query_params:
                ci = query_params["ci"][0]
                paciente = self.find_patient(ci)
                if paciente:
                    self.response_handler(200, [paciente])
                else:
                    self.response_handler(204, [])
            elif "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = [
                    paciente
                    for paciente in pacientes
                    if paciente["Diagnostico"] == diagnostico
                ]
                if pacientes_filtrados:
                    self.response_handler(200, pacientes_filtrados)
                else:
                    self.response_handler(204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = [
                    paciente
                    for paciente in pacientes
                    if paciente["Doctor"] == doctor
                ]
                if pacientes_filtrados:
                    self.response_handler(200, pacientes_filtrados)
                else:
                    self.response_handler(204, [])
            else:
                self.response_handler(200, pacientes)
        elif parsed_path.path.startswith("/pacientes/"):
            ci = parsed_path.path.split("/")[-1]
            paciente = self.find_patient(ci)
            if paciente:
                self.response_handler(200, [paciente])
            else:
                self.response_handler(204, [])
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    
    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes.append(data)
            self.response_handler(201, pacientes)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            paciente = self.find_patient(ci)
            data = self.read_data()
            if paciente:
                paciente.update(data)
                self.response_handler(200, [pacientes])
            else:
                self.response_handler(404, {"Error": "Paciente no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[-1]
            paciente = self.find_patient(ci)
            if paciente:
                pacientes.remove(paciente)
                self.response_handler(200, pacientes)
            else:
                self.response_handler(404, {"Error": "Paciente no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
