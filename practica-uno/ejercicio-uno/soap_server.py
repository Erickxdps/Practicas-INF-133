from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def SumaDosNumeros(numero1, numero2):
    return {"resultado": numero1 + numero2}

def RestaDosNumeros(numero1, numero2):
    return {"resultado": numero1 - numero2}

def MultiplicarDosNumeros(numero1, numero2):
    return {"resultado": numero1 * numero2}

def DividirDosNumeros(numero1, numero2):
    if numero2 == 0:
        return {"error": "División por cero"}
    return {"resultado": numero1 / numero2}

dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)


dispatcher.register_function(
    "SumaDosNumeros",
    SumaDosNumeros,
    returns={"resultado": int},
    args={"numero1": int, "numero2": int},
)
dispatcher.register_function(
    "RestaDosNumeros",
    RestaDosNumeros,
    returns={"resultado": int},
    args={"numero1": int, "numero2": int},
)
dispatcher.register_function(
    "MultiplicarDosNumeros",
    MultiplicarDosNumeros,
    returns={"resultado": int},
    args={"numero1": int, "numero2": int},
)
dispatcher.register_function(
    "DividirDosNumeros",
    DividirDosNumeros,
    returns={"resultado": float},
    args={"numero1": int, "numero2": int},
)

server = HTTPServer(("", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciando en http://localhost:8000/")
server.serve_forever()
