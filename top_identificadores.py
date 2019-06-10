import json
from datetime import datetime
import codigos_hex

def contador(nombre_numero):
  """Devuelve el numero (valor) de transacciones de un protocolo (nombre) pertenecientes a un diccionario clave/valor dados como tupla"""
  return nombre_numero[1]	 

def main():
 	"""Programa que devuelve los 2 primeros bytes en hexadecimal de los protocolos mas repetidos en las transacciones OP_RETURN"""
	
	# Lugar del que obtenemos las transacciones OP_RETURN en bruto
	dir = 'archivos_formateados/'

	# Variables inicializadas que usare
	inicio = 0;
	final =  300000 #578703
	codigos = {}
	
	# Cargar contenido archivos
	for i in range (inicio,final):
	    with open(dir + str(i) + '.json') as f:
	        datos = json.load(f)
 
  			# Bloque CON TXs OP_RETURN
	        if datos['op_returns'] != []:
		        for transaccion in datos['op_returns']:

		        	# Buscamos encontrar coicidencias en las cadenas hexadecimales para encontrar e identificar los protocolos mas repetidos
		       		if transaccion['hex'][0:4] not in codigos:
		       			codigos[transaccion['hex'][0:4]] = 1
		       		else:
		       			codigos[transaccion['hex'][0:4]] = codigos[transaccion['hex'][0:4]] + 1
	    
	    f.close()
	    #print i
  	
  	# Ordenamos los protocolos por el que tenga mayor numero de transacciones en los mismos
  	items = sorted(codigos.items(), key=contador, reverse=True)
	
	# Imprimimos los primeros bytes que identificarian los 20 protocolos mas usados
  	for item in items[:20]:
  		print 'COD_HEX:', item[0], '\t#TXs:', item[1]

if __name__ == '__main__':
  main()