import sys
import os
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
	final =  578704 #578703
	reconocidas = 0
	bloques_con_opreturns = 0
	bloques_sin_opreturns = 0
	
	#if "LP_UNKNOWN" in codigos_hex.Codigos.__members__:
	#	print 'Comente en codigos_hex.py el ultimo protocolo (LP_UNKNOWN)'
	#	sys.exit()

	protocolos_TXs = {}
	for codigo in codigos_hex.Codigos:
		if codigo.name not in protocolos_TXs:
			protocolos_TXs[codigo.name] = 0
	num_protocolos_conocidos = len(protocolos_TXs)

	protocolos_tamano = {}
	for codigo in codigos_hex.Codigos:
		if codigo.name not in protocolos_tamano:
			protocolos_tamano[codigo.name] = 0

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

		    		for codigo in codigos_hex.Codigos:	       
		    			# Codigo hexadecimal de la transaccion reconocido -> Protocolo Identificado 
		    			# Si coinciden se acumulan las TXs  y el tamano de TX pertenecientes al protocolo
		        		if codigo.value in transaccion['hex']:
			        		protocolos_TXs[codigo.name] = protocolos_TXs[codigo.name] + 1
			        		protocolos_tamano[codigo.name] = protocolos_tamano[codigo.name] + bytes_transaccion
			       			reconocidas = reconocidas + 1 

		    # Bloque SIN Txs OP_RETURN
	        else:
	        	bloques_sin_opreturns = bloques_sin_opreturns + 1

	        print 'Bloque',i, 'leido'

	    f.close()  
  	
	# Si las carpetas no estan creadas, genero las carpetas donde se almacenaran los graficos producidos por el programa
	dir = 'diagramas'
	if not os.path.exists(dir):
		os.mkdir(dir)
	if not os.path.exists('diagramas/opreturn'):
		os.mkdir('diagramas/opreturn')
	if not os.path.exists('diagramas/opreturn/anexos'):
		os.mkdir('diagramas/opreturn/anexos')	



  	# GRAFICO CIRCULAR PROTOCOLOS-TXS por numero de transacciones
  	# Ordeno los protocolos por el mayor numero de transacciones en los mismos
  	lista_protocolos = sorted(protocolos_TXs.items(), key=contador, reverse=True)
	protocolos = []
 	num_TXs = []

  	# Convierto la estructura diccionario en listas para dibujar el grafico
	print '\nProtocolo - num-TXs:'
  	for nombre, numero in lista_protocolos:
  		protocolos.append(nombre)
  		num_TXs.append(numero)
  		print nombre,' - ', numero

	# Dibujo el diagrama circular ayudandome de la libreria plotly
	plotly.offline.plot({
    	"data": [go.Pie(labels=protocolos, values=num_TXs, hoverinfo='label+value')],
    	"layout": go.Layout(title={'text' : "Protocolos (SIN UNKNOWN) / Numero de Transacciones", 'font' : dict(size=40)})
		},filename='diagramas/opreturn/anexos/protocolos-TXs-numero_SIN_UNKNOWN.html', auto_open=True)

	# GRAFICO CIRCULAR CATEGORIAS-TXS y CERTIFICACIONES-TXs por numero de transacciones
	# Inicializamos los categorias en las que vamos agrupar los protocolos
	lista_categorias =  {'ARTE DIGITAL' : 0, 'BIENES' : 0, 'DOCUMENTOS NOTARIALES': 0, 'OTROS': 0}
	lista_certificaciones = {'SI' : 0, 'NO' : 0}

	# Agrupamos los protocolos en categorias
	for nombre, numero in protocolos_TXs.items():

		# ARTE DIGITAL
		if (nombre == codigos_hex.Codigos.ASCRIBE.name or nombre == codigos_hex.Codigos.MONEGRAPH.name):
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
		or nombre == codigos_hex.Codigos.PROOFOFEXISTENCE.name or nombre == codigos_hex.Codigos.PROVEBIT.name or nombre == codigos_hex.Codigos.STAMPD.name 
		or nombre == codigos_hex.Codigos.STAMPERY.name):
			lista_categorias['DOCUMENTOS NOTARIALES'] = lista_categorias['DOCUMENTOS NOTARIALES'] + numero
			lista_certificaciones['SI'] = lista_certificaciones['SI'] + numero
		
		# OTROS
		elif (nombre == codigos_hex.Codigos.BLOCKSTORE.name or nombre == codigos_hex.Codigos.ETERNITYWALL.name or nombre == codigos_hex.Codigos.SMARTBIT.name):
			lista_categorias['OTROS'] = lista_categorias['OTROS'] + numero
			lista_certificaciones['NO'] = lista_certificaciones['NO'] + numero
  		
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
    	"data": [go.Pie(labels=categorias, values=num_categorias,  textfont=dict(size=16), hoverinfo='label+value', textinfo='label+percent')],
    	"layout": go.Layout(title={'text' : "Categorias (SIN UNKNOWN) / Numero de Transacciones",'font' : dict(size=25)})
		},filename='diagramas/opreturn/anexos/categorias-TXs-numero_SIN_UNKNOWN.html', auto_open=True)	

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
    	"data": [go.Pie(labels=certificaciones, values=num_certificaciones, textfont=dict(size=20), hoverinfo='label+value', textinfo='label+percent')],
    	"layout": go.Layout(title={'text' : "Transacciones (Numero) que certifican informacion (SIN UNKNOWN)",'font' : dict(size=25)})
		},filename='diagramas/opreturn/anexos/certificaciones-TXs-numero_SIN_UNKNOWN.html', auto_open=True)	



	# GRAFICO DE BARRAS PROTOCOLOS-TXS por tamano de las transacciones
	# Ordeno los protocolos por el mayor numero de transacciones en los mismos
	lista_protocolos2 = sorted(protocolos_tamano.items(), key=contador, reverse=True)
 	protocolos2 = []
 	tamano_TXs = []

  	# Convierto la estructura diccionario en listas para dibujar el grafico
  	print '\nProtocolo - tamano-TXs:'
  	for nombre, numero in lista_protocolos2:
  		protocolos2.append(nombre)
  		tamano_TXs.append(numero)
  		print nombre, ' - ', numero, 'bytes'


  	# Dibujo el diagrama de barras ayudandome de la libreria plotly
	traza = go.Bar(x=protocolos2, y=tamano_TXs, hoverinfo='x+y')
	layout = {
		'title' : { 
			'text' : "Protocolos (SIN UNKNOWN) / Tamano de Transacciones (M = MBs)",
			'font' : dict(size=40)
		},
		'xaxis': {
			'title' : 'Protocolos',
			'titlefont' : dict(size=22),
			'tickfont' : dict(size=14)
	    },
	    'yaxis': {
	    	'title' : 'Tamano Transacciones (M = MBs)',
			'titlefont' : dict(size=22),
			'tickfont' : dict(size=20),
	    }
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	plotly.offline.plot(fig,filename='diagramas/opreturn/anexos/protocolos-TXs-tamano_SIN_UNKNOWN.html', auto_open=True)	



	
	# GRAFICO DE BARRAS CATEGORIAS-TXS por tamano de las transacciones
	# Inicializamos los categorias en las que vamos agrupar los protocolos
	lista_categorias =  {'ARTE DIGITAL' : 0, 'BIENES' : 0, 'DOCUMENTOS NOTARIALES': 0, 'OTROS': 0}

	# Agrupamos los protocolos en categorias
	for nombre, numero in protocolos_tamano.items():

		# ARTE DIGITAL
		if (nombre == codigos_hex.Codigos.ASCRIBE.name or nombre == codigos_hex.Codigos.MONEGRAPH.name):
			lista_categorias['ARTE DIGITAL'] = lista_categorias['ARTE DIGITAL'] + numero
			
		# BIENES
		elif (nombre == codigos_hex.Codigos.COINSPARK.name or nombre == codigos_hex.Codigos.COLU.name or nombre == codigos_hex.Codigos.COUNTERPARTY.name
		or nombre == codigos_hex.Codigos.OMNI.name or nombre == codigos_hex.Codigos.OPENASSETS.name):
			lista_categorias['BIENES'] = lista_categorias['BIENES'] + numero
	
		# DOCUMENTOS NOTARIALES
		elif (nombre == codigos_hex.Codigos.BITPROOF.name or nombre == codigos_hex.Codigos.BLOCKSIGN.name or nombre == codigos_hex.Codigos.CRYPTOCOPYRIGHT.name 
		or nombre == codigos_hex.Codigos.FACTOM.name or nombre == codigos_hex.Codigos.LAPREUVE.name or nombre == codigos_hex.Codigos.NICOSIA.name
		or nombre == codigos_hex.Codigos.PROOFOFEXISTENCE.name or nombre == codigos_hex.Codigos.PROVEBIT.name or nombre == codigos_hex.Codigos.STAMPD.name 
		or nombre == codigos_hex.Codigos.STAMPERY.name):
			lista_categorias['DOCUMENTOS NOTARIALES'] = lista_categorias['DOCUMENTOS NOTARIALES'] + numero
	
		# OTROS
		elif (nombre == codigos_hex.Codigos.BLOCKSTORE.name or nombre == codigos_hex.Codigos.ETERNITYWALL.name or nombre == codigos_hex.Codigos.SMARTBIT.name):
			lista_categorias['OTROS'] = lista_categorias['OTROS'] + numero
		
  	# CATEGORIAS
  	categorias = []
 	tamano_categorias = []
	
	print '\nCategorias - tamano-TXs:'
	for nombre, numero in lista_categorias.items():
  		categorias.append(nombre)
  		tamano_categorias.append(numero)
		print nombre, ' - ', numero, 'bytes'

	# Dibujo el diagrama de barras ayudandome de la libreria plotly
	traza = go.Bar(x=categorias, y=tamano_categorias, hoverinfo='x+y')
	layout = {
		'title' : { 
			'text' : "Categorias (SIN UNKNOWN) / Tamano de Transacciones (M = MBs)",
			'font' : dict(size=40)
		},
		'xaxis': {
			'title' : 'Categorias',
			'titlefont' : dict(size=22),
			'tickfont' : dict(size=14)
	    },
	    'yaxis': {
	    	'title' : 'Tamano Transacciones (M = MBs)',
			'titlefont' : dict(size=22),
			'tickfont' : dict(size=20),
	    }
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	plotly.offline.plot(fig,filename='diagramas/opreturn/anexos/categorias-TXs-tamano_SIN_UNKNOWN.html', auto_open=True)	



	# GRAFICO DE BARRAS PROTOCOLOS-TXS por tamano medio de TXs
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

	# Dibujo el diagrama de barras ayudandome de la libreria plotly
	traza = go.Bar(x=nombre_protocolos, y=media_TX, hoverinfo='x+y')
	layout = {
		'title' : { 
			'text' : "Protocolos (SIN UNKNOWN) / Tamano Medio TX (bytes)",
			'font' : dict(size=40)
		},
		'xaxis': {
			'tickfont' : dict(size=14)
	    },
	    'yaxis': {
	    	'title' : 'Tamano Medio TX (bytes)',
			'titlefont' : dict(size=25),
			'tickfont' : dict(size=20)
	    }
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	plotly.offline.plot(fig,filename='diagramas/opreturn/anexos/protocolos-tamano-medio-TXs_SIN_UNKNOWN.html', auto_open=True)	

	# GRAFICO DE BARRAS PROTOCOLOS-TXS agrupados en CATEGORIAS por tamano medio de TXs
	trace1 = go.Bar(
	    x=[nombre_protocolos[0],nombre_protocolos[11]],
	    y=[media_TX[0],media_TX[11]],
	    hoverinfo='x+y',
	    name='ARTE_DIGITAL'
	)

	trace2 = go.Bar(
	    x=[nombre_protocolos[4],nombre_protocolos[5],nombre_protocolos[6],nombre_protocolos[13],nombre_protocolos[14]],
	    y=[media_TX[4],media_TX[5],media_TX[6],media_TX[13],media_TX[14]],
		hoverinfo='x+y',
		name='BIENES'
	)

	trace3 = go.Bar(
		x=[nombre_protocolos[1],nombre_protocolos[2],nombre_protocolos[10],nombre_protocolos[9],nombre_protocolos[7],
			nombre_protocolos[12],nombre_protocolos[15],nombre_protocolos[16],nombre_protocolos[18],nombre_protocolos[19]],
	    y=[media_TX[1],media_TX[2],media_TX[10],media_TX[9],media_TX[7],
	    	media_TX[12],media_TX[15],media_TX[16],media_TX[18],media_TX[19]],
    	hoverinfo='x+y',
	    name='DOCUMENTOS_NOTARIALES'	    
	)

	trace4 = go.Bar(
	    x=[nombre_protocolos[3],nombre_protocolos[8],nombre_protocolos[17]],
	    y=[media_TX[3],media_TX[8],media_TX[17]],
	    hoverinfo='x+y',
	    name='OTROS'
	)

	data = [trace1,trace2,trace3,trace4]
	layout = {
		'title' : { 
			'text' : "Protocolos Categorizados (SIN UNKNOWN) / Tamano Medio TX (bytes)",
			'font' : dict(size=40)
		},
		'xaxis': {
			'title' : 'Protocolos',
			'titlefont' : dict(size=25),
			'tickfont' : dict(size=14)
	    },
	    'yaxis': {
	    	'title' : 'Tamano Medio TX (bytes)',
			'titlefont' : dict(size=25),
			'tickfont' : dict(size=20)
	    },
	    'barmode' : 'group'
	}

	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig, filename='diagramas/opreturn/anexos/protocolos-tamano-medio-TXs-grouped_SIN_KNOWN.html')



	# Imprimimos informacion recabada
  	print '\nINFORMACION RESUMIDA:'
  	print 'Bloques procesados', final
	print 'Bloques con TXs OP_RETURN', bloques_con_opreturns
	print 'Bloques sin TXs OP_RETURN', bloques_sin_opreturns
 	print 'Numero de Protocolos Conocidos:', num_protocolos_conocidos
  	print 'TXs Reconocidas:', reconocidas
  	tamano_total = 0
	for tamano in tamano_TXs:
		tamano_total = tamano_total + tamano*1.0
	print 'Tamano Total:', tamano_total, 'bytes'
	print 'Tamano Medio TX: {0:.2f}'.format(tamano_total / reconocidas), 'bytes/tx'

if __name__ == '__main__':
  main()