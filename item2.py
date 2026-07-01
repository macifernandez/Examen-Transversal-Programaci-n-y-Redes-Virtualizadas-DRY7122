import urllib.parse
import requests

api_principal = "https://graphhopper.com/api/1"
clave = "50a10580-dbfe-4c91-8b23-26dc45a37789"

def geocodificacion(ubicacion, clave):
    url_geocode = api_principal + "/geocode?"
    url = url_geocode + urllib.parse.urlencode({
        "q": ubicacion,
        "limit": "1",
        "key": clave
    })

    respuesta = requests.get(url)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and len(datos["hits"]) != 0:
        latitud = datos["hits"][0]["point"]["lat"]
        longitud = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]
        pais = datos["hits"][0]["country"]

        return estado, latitud, longitud, nombre + ", " + pais
    else:
        print("No se encontró la ubicación.")
        return estado, None, None, ubicacion


while True:

    print("\n==============================")
    print("MEDIOS DE TRANSPORTE")
    print("==============================")
    print("car")
    print("bike")
    print("foot")
    print("==============================")

    transporte = input("Ingrese el medio de transporte (o s para salir): ")

    if transporte.lower() == "s":
        break

    if transporte not in ["car", "bike", "foot"]:
        print("Medio de transporte no válido.")
        continue

    origen = input("Ciudad de Origen : ")

    if origen.lower() == "s":
        break

    destino = input("Ciudad de Destino : ")

    if destino.lower() == "s":
        break

    origen_geo = geocodificacion(origen, clave)
    destino_geo = geocodificacion(destino, clave)

    if origen_geo[0] == 200 and destino_geo[0] == 200:

        punto_origen = "&point=" + str(origen_geo[1]) + "%2C" + str(origen_geo[2])
        punto_destino = "&point=" + str(destino_geo[1]) + "%2C" + str(destino_geo[2])

        url_ruta = api_principal + "/route?"

        ruta = url_ruta + urllib.parse.urlencode({
            "key": clave,
            "vehicle": transporte
        }) + punto_origen + punto_destino

        respuesta = requests.get(ruta)
        datos = respuesta.json()

        if respuesta.status_code == 200:

            kilometros = datos["paths"][0]["distance"] / 1000
            millas = kilometros / 1.61

            segundos = int(datos["paths"][0]["time"] / 1000)

            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            segundos = segundos % 60

            print("\n===================================")
            print("RESULTADO DEL VIAJE")
            print("===================================")
            print("Origen:", origen_geo[3])
            print("Destino:", destino_geo[3])
            print("Transporte:", transporte)
            print("Distancia en kilómetros: {:.2f}".format(kilometros))
            print("Distancia en millas: {:.2f}".format(millas))
            print("Duración: {:02d}:{:02d}:{:02d}".format(horas, minutos, segundos))

            print("\nNarrativa del viaje:")

            for paso in datos["paths"][0]["instructions"]:
                print("-", paso["text"])

        else:
            print("Error:", datos["message"])