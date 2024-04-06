from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Lista para almacenar la información de los mensajes
mensajes = []


class RESTRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def find_message_by_id(self, message_id):
        return next(
            (message for message in mensajes if message["ID"] == message_id),
            None,
        )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

    def encrypt_message(self, cadena):
        siu = False
        resultado = ""
        for letra in cadena:
            if letra.isalpha():
                if letra.isupper():
                    letra = letra.lower()
                    siu = True
                n = ord(letra)
                if n > 109:
                    a = chr(n - 13)
                else:
                    a = chr(n + 13)
                
                if siu:
                    a = a.upper()
                    siu = False        
                resultado += a
            else:
                resultado = resultado + letra
        return resultado
    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            contenido = data.get("Contenido", "")
            encrypted_contenido = self.encrypt_message(contenido)
            mensaje = {
                "ID": str(len(mensajes) + 1),
                "Contenido": contenido,
                "Contenido encriptado": encrypted_contenido,
            }
            mensajes.append(mensaje)
            self.response_handler(201, mensaje)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_GET(self):
        if self.path == "/mensajes":
            self.response_handler(200, mensajes)
        elif self.path.startswith("/mensajes/"):
            message_id = self.path.split("/")[-1]
            mensaje = self.find_message_by_id(message_id)
            if mensaje:
                self.response_handler(200, mensaje)
            else:
                self.response_handler(204, [])
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            message_id = self.path.split("/")[-1]
            mensaje = self.find_message_by_id(message_id)
            if mensaje:
                data = self.read_data()
                nuevo_contenido = data.get("Contenido", "")
                encrypted_nuevo_contenido = self.encrypt_message(nuevo_contenido)
                mensaje["Contenido"] = nuevo_contenido
                mensaje["Contenido encriptado"] = encrypted_nuevo_contenido
                self.response_handler(200, mensaje)
            else:
                self.response_handler(404, {"Error": "Mensaje no encontrado"})
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            message_id = self.path.split("/")[-1]
            mensaje = self.find_message_by_id(message_id)
            if mensaje:
                mensajes.remove(mensaje)
                self.response_handler(200, {"Mensaje eliminado": mensaje})
            else:
                self.response_handler(404, {"Error": "Mensaje no encontrado"})
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
