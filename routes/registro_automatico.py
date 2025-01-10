import threading
import time
import requests
from datetime import datetime

def llamar_registro_automatico():
    while True:
        ahora = datetime.now()
        if ahora.hour == 20 and ahora.minute == 28:
            try:
                # Realiza la llamada HTTP al servidor Flask
                response = requests.post("http://localhost:5000/registrar_entrada_automatica")
                if response.status_code == 200:
                    print("Registro automático exitoso.")
                else:
                    print("Error en el registro automático:", response.text)
            except Exception as e:
                print("Error al llamar al servidor Flask:", e)

            # Espera un minuto para evitar llamar varias veces en el mismo minuto
            time.sleep(60)
        else:
            # Verifica cada 30 segundos
            time.sleep(30)
