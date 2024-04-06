from zeep import Client

client = Client('http://localhost:8000')

numero1 = 10;numero2=5
suma = client.service.SumaDosNumeros(numero1, numero2)
print(f"La suma del {numero1} con el {numero2} dara de resultado : {suma}")
numero1 = 10;numero2=5
resta = client.service.RestaDosNumeros(numero1, numero2)
print(f"La resta del {numero1} con el {numero2} dara de resultado : {resta}")
numero1 = 10;numero2=5
multiplicacion = client.service.MultiplicarDosNumeros(numero1, numero2)
print(f"La multiplicacion del {numero1} con el {numero2} dara de resultado : {multiplicacion}")
numero1 = 10;numero2=5
dividir = client.service.DividirDosNumeros(numero1, numero2)
print(f"La dividir del {numero1} con el {numero2} dara de resultado : {dividir}")
