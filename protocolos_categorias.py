import os
import sys
import json
import codigos_hex
import plotly
import plotly.graph_objs as go

def contador(nombre_numero):
  """Devuelve el numero (valor) de transacciones de un protocolo (clave o nombre), pertenecientes a un diccionario clave/valor dados como tupla"""
  return nombre_numero[1]	 

def main():
	"""Programa que genera diagramas con los protocolos y las categorias principales de OP_RETURN"""

	# Lugar del que obtenemos las transacciones OP_RETURN en bruto
	dir = 'archivos_formateados/'

	# Variables inicializadas que usare
	inicio = 0
	final =  300000 #578703
	reconocidas = 0
	bloques_con_opreturns = 0
	bloques_sin_opreturns = 0

	if "LP_UNKNOWN" not in codigos_hex.Codigos.__members__:
		print 'Descomente en codigos_hex.py el ultimo protocolo (LP_UNKNOWN)'
		sys.exit()

	protocolos_TXs = {}
	for codigo in codigos_hex.Codigos:
		if codigo.name not in protocolos_TXs:
			protocolos_TXs[codigo.name] = 0	
	num_protocolos_conocidos = len(protocolos_TXs)
	protocolos_TXs['UNKNOWN'] = 0
	
	protocolos_tamano = {}
	for codigo in codigos_hex.Codigos:
		if codigo.name not in protocolos_tamano:
			protocolos_tamano[codigo.name] = 0
	protocolos_tamano['UNKNOWN'] = 0

	# Cargar contenido archivos
	for i in range (inicio,final):
		with open(dir + str(i) + '.json') as f:
			datos = json.load(f)
			
			# Bloque CON TXs OP_RETURN	
			if datos['op_returns'] != []:
				
				bloques_con_opreturns = bloques_con_opreturns + 1	

				for transaccion in datos['op_returns']:

					# El tamano en bytes de una transaccion OP_RETURN se halla tomando un byte por cada digito hexadecimal
					bytes_transaccion = len(transaccion['hex'])/2
					codigo_hex_abrev = transaccion['hex'][0:4]
					desconocida = True

					for codigo in codigos_hex.Codigos:	       
						# Codigo hexadecimal de la transaccion reconocido -> Protocolo Identificado 
						# Si coinciden se acumulan las TXs  y el tamano de TX pertenecientes al protocolo
						if codigo_hex_abrev in codigo.value[0:4]:
							protocolos_TXs[codigo.name] = protocolos_TXs[codigo.name] + 1
							protocolos_tamano[codigo.name] = protocolos_tamano[codigo.name] + bytes_transaccion
							reconocidas = reconocidas + 1 
							desconocida = False

					# Caso TXs UNKNOWN
					if desconocida:
						protocolos_TXs['UNKNOWN'] = protocolos_TXs['UNKNOWN'] + 1
						protocolos_tamano['UNKNOWN'] = protocolos_tamano['UNKNOWN'] + bytes_transaccion
					

			# Bloque SIN Txs OP_RETURN
			else:
				bloques_sin_opreturns = bloques_sin_opreturns + 1

			print i

		f.close()  
	
	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = 'diagramas'
	if not os.path.exists(dir):
		os.mkdir(dir)
	if not os.path.exists('diagramas/opreturn'):
		os.mkdir('diagramas/opreturn')


	# GRAFICO CIRCULAR PROTOCOLOS-TXS por numero de transacciones
	# Ordeno los protocolos por el mayor numero de transacciones en los mismos
	lista_protocolos = sorted(protocolos_TXs.items(), key=contador, reverse=True)
	protocolos = []
	num_TXs = []

	# Creo un fichero de datos para utilizarlo con otro programa de descentralizacion mas adelante
	with open('data/protocolos_TXs.data','w') as f:
		f.close()
	
	# Convierto la estructura diccionario en listas para dibujar el grafico
	print '\nProtocolo - num-TXs:'
	for nombre, numero in lista_protocolos:
		protocolos.append(nombre)
		num_TXs.append(numero)
		# Muestro por pantalla
		print nombre,' - ', numero
		# Relleno el fichero anteriormente creado de datos.
		with open('data/protocolos_TXs.data','a') as f:
			f.write(str(nombre)+' '+str(numero)+'\n')
			f.close()

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
		"data": [go.Pie(labels=protocolos, values=num_TXs, hoverinfo='label+value', textinfo='label+percent')],
		"layout": go.Layout(title="Protocolos/Numero Transacciones")
		},filename='diagramas/opreturn/protocolos-TXs-numero.html', auto_open=True)

	# GRAFICO CIRCULAR CATEGORIAS-TXS y CERTIFICACIONES-TXs por numero de transacciones
	# Inicializamos los categorias en las que vamos agrupar los protocolos
	lista_categorias =  {'ARTE DIGITAL' : 0, 'BIENES' : 0, 'DOCUMENTOS NOTARIALES': 0, 'OTROS': 0, 'UNKNOWN' : protocolos_TXs['UNKNOWN']}
	lista_certificaciones = {'SI' : 0, 'NO' : 0, 'DESC' : protocolos_TXs['UNKNOWN']}

	# Agrupamos los protocolos en categorias
	for nombre, numero in protocolos_TXs.items():

		# ARTE DIGITAL
		if (nombre == codigos_hex.Codigos.ASCRIBE.name or nombre == codigos_hex.Codigos.BLOCKAI.name or nombre == codigos_hex.Codigos.MONEGRAPH.name):
			lista_categorias['ARTE DIGITAL'] = lista_categorias['ARTE DIGITAL'] + numero
			lista_certificaciones['SI'] = lista_certificaciones['SI'] + numero

		# BIENES
		elif (nombre == codigos_hex.Codigos.COINSPARK.name or nombre == codigos_hex.Codigos.COLU.name or nombre == codigos_hex.Codigos.COUNTERPARTY.name
		or nombre == codigos_hex.Codigos.OMNI.name or nombre == codigos_hex.Codigos.OPENASSETS.name):
			lista_categorias['BIENES'] = lista_categorias['BIENES'] + numero
			lista_certificaciones['SI'] = lista_certificaciones['SI'] + numero

		# DOCUMENTOS NOTARIALES
		elif (nombre == codigos_hex.Codigos.BITPROOF.name or nombre == codigos_hex.Codigos.BLOCKSIGN.name or nombre == codigos_hex.Codigos.CRYPTOCOPYRIGHT.name 
		or nombre == codigos_hex.Codigos.FACTOM.name or nombre == codigos_hex.Codigos.LAPREUVE.name or nombre == codigos_hex.Codigos.NICOSIA.name
		or nombre == codigos_hex.Codigos.ORIGINALMY.name or nombre == codigos_hex.Codigos.PROOFOFEXISTENCE.name or nombre == codigos_hex.Codigos.PROVEBIT.name 
		or nombre == codigos_hex.Codigos.REMEMBR.name or nombre == codigos_hex.Codigos.STAMPD.name or nombre == codigos_hex.Codigos.STAMPERY.name 
		or nombre == codigos_hex.Codigos.TRADLE.name):
			lista_categorias['DOCUMENTOS NOTARIALES'] = lista_categorias['DOCUMENTOS NOTARIALES'] + numero
			lista_certificaciones['SI'] = lista_certificaciones['SI'] + numero
		
		# OTROS
		elif (nombre == codigos_hex.Codigos.BLOCKSTORE.name or nombre == codigos_hex.Codigos.ETERNITYWALL.name or nombre == codigos_hex.Codigos.SMARTBIT.name):
			lista_categorias['OTROS'] = lista_categorias['OTROS'] + numero
			lista_certificaciones['NO'] = lista_certificaciones['NO'] + numero
		
		# LP_UNKNOWN 
		elif (nombre == codigos_hex.Codigos.LP_UNKNOWN.name):
			lista_categorias['UNKNOWN'] = lista_categorias['UNKNOWN'] + numero
			lista_certificaciones['DESC'] = lista_certificaciones['DESC'] + numero

	# CATEGORIAS
	categorias = []
	num_categorias = []
	
	print '\nCategoria - num-TXs:'
	for nombre, numero in lista_categorias.items():
		categorias.append(nombre)
		num_categorias.append(numero)
		print nombre, ' - ', numero

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
		"data": [go.Pie(labels=categorias, values=num_categorias, hoverinfo='label+value', textinfo='label+percent')],
		"layout": go.Layout(title="Categorias/Numero Transacciones")
		},filename='diagramas/opreturn/categorias-TXs-numero.html', auto_open=True)

	# CERTIFICACIONES
	certificaciones = []
	num_certificaciones = []
	
	print '\nCertificaciones - num-TXs:'
	for nombre, numero in lista_certificaciones.items():
		certificaciones.append(nombre)
		num_certificaciones.append(numero)	
		print nombre, ' - ', numero

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
		"data": [go.Pie(labels=certificaciones, values=num_certificaciones, hoverinfo='label+value', textinfo='label+percent')],
		"layout": go.Layout(title="Transacciones (Numero) que certifican informacion")
		},filename='diagramas/opreturn/certificaciones-TXs-numero.html', auto_open=True)	



	# GRAFICO CIRCULAR PROTOCOLOS-TXS por tamano de las transacciones
	# Ordeno los protocolos por el mayor numero de transacciones en los mismos
	lista_protocolos2 = sorted(protocolos_tamano.items(), key=contador, reverse=True)
	protocolos2 = []
	tamano_TXs = []

	# Creo un fichero de datos para utilizarlo con otro programa de descentralizacion mas adelante
	with open('data/protocolos_Tamano.data','w') as f:
		f.close()

	# Convierto la estructura diccionario en listas para dibujar el grafico
	print '\nProtocolo - tamano-TXs:'
	for nombre, numero in lista_protocolos2:
		protocolos2.append(nombre)
		tamano_TXs.append(numero)
		# Muestro por pantalla
		print nombre, ' - ', numero, 'bytes'
		# Relleno el fichero anteriormente creado de datos.
		with open('data/protocolos_Tamano.data','a') as f:
			f.write(str(nombre)+' '+str(numero)+'\n')
			f.close()

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
		"data": [go.Pie(labels=protocolos2, values=tamano_TXs, hoverinfo='label+value', textinfo='label+percent')],
		"layout": go.Layout(title="Protocolos/Tamano Transacciones")
		},filename='diagramas/opreturn/protocolos-TXs-tamano.html', auto_open=True)

	# GRAFICO CIRCULAR CATEGORIAS-TXS y CERTIFICACIONES-TXs por tamano de las transacciones
	# Inicializamos los categorias en las que vamos agrupar los protocolos
	lista_categorias =  {'ARTE DIGITAL' : 0, 'BIENES' : 0, 'DOCUMENTOS NOTARIALES': 0, 'OTROS': 0, 'UNKNOWN' : protocolos_tamano['UNKNOWN']}
	lista_certificaciones = {'SI' : 0, 'NO' : 0, 'DESC' : protocolos_tamano['UNKNOWN']}

	# Agrupamos los protocolos en categorias
	for nombre, numero in protocolos_tamano.items():

		# ARTE DIGITAL
		if (nombre == codigos_hex.Codigos.ASCRIBE.name or nombre == codigos_hex.Codigos.BLOCKAI.name or nombre == codigos_hex.Codigos.MONEGRAPH.name):
			lista_categorias['ARTE DIGITAL'] = lista_categorias['ARTE DIGITAL'] + numero
			lista_certificaciones['SI'] = lista_certificaciones['SI'] + numero

		# BIENES
		elif (nombre == codigos_hex.Codigos.COINSPARK.name or nombre == codigos_hex.Codigos.COLU.name or nombre == codigos_hex.Codigos.COUNTERPARTY.name
		or nombre == codigos_hex.Codigos.OMNI.name or nombre == codigos_hex.Codigos.OPENASSETS.name):
			lista_categorias['BIENES'] = lista_categorias['BIENES'] + numero
			lista_certificaciones['SI'] = lista_certificaciones['SI'] + numero

		# DOCUMENTOS NOTARIALES
		elif (nombre == codigos_hex.Codigos.BITPROOF.name or nombre == codigos_hex.Codigos.BLOCKSIGN.name or nombre == codigos_hex.Codigos.CRYPTOCOPYRIGHT.name 
		or nombre == codigos_hex.Codigos.FACTOM.name or nombre == codigos_hex.Codigos.LAPREUVE.name or nombre == codigos_hex.Codigos.NICOSIA.name
		or nombre == codigos_hex.Codigos.ORIGINALMY.name or nombre == codigos_hex.Codigos.PROOFOFEXISTENCE.name or nombre == codigos_hex.Codigos.PROVEBIT.name 
		or nombre == codigos_hex.Codigos.REMEMBR.name or nombre == codigos_hex.Codigos.STAMPD.name or nombre == codigos_hex.Codigos.STAMPERY.name 
		or nombre == codigos_hex.Codigos.TRADLE.name):
			lista_categorias['DOCUMENTOS NOTARIALES'] = lista_categorias['DOCUMENTOS NOTARIALES'] + numero
			lista_certificaciones['SI'] = lista_certificaciones['SI'] + numero

		# OTROS
		elif (nombre == codigos_hex.Codigos.BLOCKSTORE.name or nombre == codigos_hex.Codigos.ETERNITYWALL.name or nombre == codigos_hex.Codigos.SMARTBIT.name):
			lista_categorias['OTROS'] = lista_categorias['OTROS'] + numero
			lista_certificaciones['NO'] = lista_certificaciones['NO'] + numero
		
		# LP_UNKNOWN 
		elif (nombre == codigos_hex.Codigos.LP_UNKNOWN.name):
			lista_categorias['UNKNOWN'] = lista_categorias['UNKNOWN'] + numero
			lista_certificaciones['DESC'] = lista_certificaciones['DESC'] + numero

	# CATEGORIAS
	categorias = []
	tamano_categorias = []
	
	print '\nCategorias - tamano-TXs:'
	for nombre, numero in lista_categorias.items():
		categorias.append(nombre)
		tamano_categorias.append(numero)
		print nombre, ' - ', numero, 'bytes'

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
		"data": [go.Pie(labels=categorias, values=tamano_categorias, hoverinfo='label+value', textinfo='label+percent')],
		"layout": go.Layout(title="Categorias/Tamano Transacciones")
		},filename='diagramas/opreturn/categorias-TXs-tamano.html', auto_open=True)	

	# CERTIFICACIONES
	certificaciones = []
	tamano_certificaciones = []
	
	print '\nCertificaciones - tamano-TXs:'
	for nombre, numero in lista_certificaciones.items():
		certificaciones.append(nombre)
		tamano_certificaciones.append(numero)		
		print nombre, ' - ', numero, 'bytes'

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
		"data": [go.Pie(labels=certificaciones, values=tamano_certificaciones, hoverinfo='label+value', textinfo='label+percent')],
		"layout": go.Layout(title="Transacciones (Tamano) que certifican informacion")
		},filename='diagramas/opreturn/certificaciones-TXs-tamano.html', auto_open=True)

	# GRAFICO CIRCULAR PROTOCOLOS-TXS por tamano medio de TXs
	media_TX = []

	# Ordeno las protocolos alfabeticamente
	protocolos_TXs_ordenada = sorted(protocolos_TXs.items())
	nombre_protocolos = []
	num_TXs_protocolos = []
	# Convierto la estructura diccionario en listas para dibujar el grafico
	for nombre, numero in protocolos_TXs_ordenada:
		nombre_protocolos.append(nombre)
		num_TXs_protocolos.append(numero)

	# Ordeno las protocolos alfabeticamente
	protocolos_tamano_ordenada = sorted(protocolos_tamano.items())
	tamano_TXs_protocolos = []
	# Convierto la estructura diccionario en listas para dibujar el grafico
	for nombre, tamano in protocolos_tamano_ordenada:
		tamano_TXs_protocolos.append(tamano)

	print '\nProtocolo - media-TX:'
	k = 0
	while k < len(protocolos_TXs_ordenada):
		media_TX.append(round(tamano_TXs_protocolos[k]/(num_TXs_protocolos[k]*1.0),2))
		print nombre_protocolos[k], ' - ', media_TX[k], 'bytes/tx'
		k = k +	1

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
		"data": [go.Pie(labels=nombre_protocolos, values=media_TX, hoverinfo='label+value', textinfo='label+value')],
		"layout": go.Layout(title="Protocolos Tamano Medio TX")
		},filename='diagramas/opreturn/protocolos-tamano-medio-TXs.html', auto_open=True)



	# Imprimimos informacion recabada
	print '\nINFORMACION RESUMIDA:'
	print 'Bloques procesados:', final
	print 'Bloques con TXs OP_RETURN:', bloques_con_opreturns
	print 'Bloques sin TXs OP_RETURN:', bloques_sin_opreturns
	print 'Numero de Protocolos Conocidos:', num_protocolos_conocidos
	print 'TXs Reconocidas:', reconocidas
	print 'TXs Desconocidas:', protocolos_TXs['UNKNOWN']
	print 'Total TXs OP_RETURN:', reconocidas + protocolos_TXs['UNKNOWN']
	tamano_total = 0
	for tamano in tamano_TXs:
		tamano_total = tamano_total + tamano*1.0
	print 'Tamano Total:', tamano_total, 'bytes'
	print 'Tamano Medio TX: {0:.2f}'.format(tamano_total / (reconocidas + protocolos_TXs['UNKNOWN'])), 'bytes/tx'


if __name__ == '__main__':
  main()
