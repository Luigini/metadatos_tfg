import json
import requests
import os
import time

def main():
    """Programa para obtener los bloques de Bitcoin"""
    
    # Directorio donde guardaremos los bloques
    dir = 'archivos_formateados/'
    if not os.path.exists(dir):
        os.mkdir(dir)

    # Variables inicializadas que usare
    inicio = 0
    final = 578704 #578703

    #Creacion de archivos .json semejantes a un diccionario
    for i in range (inicio,final):
        bloque = str(i)
   
        # Hacemos una request para obtener el bloque
        peticion = 'http://api.coinsecrets.org/block/' + bloque
        resp = requests.get(peticion)
        #time.sleep(1)
        datos_bloque = resp.json()

        # Abrimos un archivo y volcamos la informacion formateada
        with open(dir + bloque + '.json', 'w') as file_dict:
            json.dump(datos_bloque, file_dict, indent = 4)
        file_dict.close()

        print 'Bloque',bloque, 'almacenado'

if __name__ == '__main__':
  main()