import os
import json
import datetime
import plotly 
import plotly.graph_objs as go

def main():
 	"""Diagrama de lineas con las transacciones OP_RETURN acumuladas en cada mes comparadas con las totales 
	de la blockchain de Bitcoin"""
	
	# Lugar del que obtenemos las transacciones OP_RETURN en bruto
	dir = '/home/donvito/Escritorio/metadatos/archivos_formateados/'

	# Variables inicializadas que usarem
	inicio = 0
	final = 578704 #578703
	transacciones_bloque = {}
 	fechas = []
 	transacciones = []

	# Cargar contenido archivos
	for i in range (inicio,final):
	    with open(dir + str(i) + '.json') as f:
	        datos = json.load(f)
	     
	     	# Tomo la marca de tiempo de los bloques en los que haya TXs OP_RETURN
	        timestamp = datos['timestamp']
	        if timestamp:
	        	# Transformo la fecha y la formateo extrayendo el anyo y el mes
	        	fecha = datetime.datetime.fromtimestamp(float(timestamp)).isoformat()
	        	fecha_formateada = fecha[:7]

	        	# Ordeno las fechas de cada TX OP_RETURN por meses en una variable diccionario
	        	if fecha_formateada not in transacciones_bloque.keys():
	        		transacciones_bloque[fecha_formateada] = len(datos['op_returns'])
	        	else:
	        		transacciones_bloque[fecha_formateada] = transacciones_bloque[fecha_formateada] + len(datos['op_returns'])
     	  	
     	  	#print i

	    f.close()  

	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = 'diagramas'
	if not os.path.exists(dir):
		os.mkdir(dir)
	if not os.path.exists('diagramas/opreturn'):
		os.mkdir('diagramas/opreturn')
		
	# Ordeno los meses e imprimimos el numero de transacciones  de cada uno de ellos
	for fecha, transaccion in sorted(transacciones_bloque.items()):
		fechas.append(fecha)
  		transacciones.append(transaccion)
  		print fecha, transaccion
  	
  	# Datos obtenido de la web https://opreturn.org/script-types/ tras haber comprobado su validez
  	num_TXs_Bitcoin = [4194563,4906506,2945483,3997104,3763602,4092613,5016493,5315413,5166860,5582851,
  					6479482,5962351,6148859,5943278,6236341,6650240,6822142,7480501,7819358,8377291,
  					8879385,8753297,9281970,9383448,9878664,11382747,19838788,15429912,13171016,11868842,
  					13553920,16517439,16662910,17339945,16473559,17281664,18073209,18241909,16579017,17398449,
  					16499350,18175654,19737948,20323618,20902964,19773273,22018738,21635641,24804799,20751915,
  					18945930,20475155,19252972,22985212,25120209,30666017,25721328,15053503,15875972,16049120,
  					17011572,15872364,17340552,18137363,17790418,19359440,20077263,20203575,22242070,22204466,
  					23729106,27612620,30280871];
	precio_bitcoin = []

	# Los datos que he parseado los he obtenido desde la web https://es.investing.com/crypto/bitcoin/btc-usd-historical-data
	with open('data/historico_bitcoin.data') as f:
		while True:
			line = f.readline()
			# Longitud cero indica final de fichero
			if len(line) == 0:
				break
			#Partimos la linea y guardamos el precio de Bitcoin cada mes
			lista = line.split()
			precio_bitcoin.append(float(lista[1]))

	# DIAGRAMA LINEAL comparando #TXs OP_RETURN respecto a #TXs BITCOIN desde el inicio OP_RETURN,
	# Ademas dibujo la evolucion del precio de Bitcoin en ese tiempo mediante otro eje
	eje_x = []
	for i in range(len(fechas)):
		eje_x.append(i)

	traza1 = go.Scatter(x=eje_x, y=transacciones, mode='lines+markers', hoverinfo='y', name='TXs OP_RETURN')
	traza2 = go.Scatter(x=eje_x, y=num_TXs_Bitcoin, mode='lines+markers', hoverinfo='y', name='TXs BITCOIN')
	traza3 = go.Scatter(x=eje_x, y=precio_bitcoin, mode='lines+markers', hoverinfo='y', name='Precio_BITCOIN($)', 
		yaxis='y2', line = dict(color = ('rgb(203, 50, 52)'), width = 4))

	layout = {
		'title' : { 
			'text' : "TXs Bitcoin, TXs OP_RETURN y Evolucion del Precio en $ de Bitcoin",
			'font' : dict(size=40)	
		},
		'xaxis': {
			'tickfont' : dict(size=25),
        	'tickmode' : 'array',
       		'tickvals' : [0, 8, 19, 31, 43, 55, 67, 72],
        	'ticktext' : ['Marzo13','2014','2015','2016','2017','2018','2019','Mayo19']
	    },
	    'yaxis': {
	    	'title' : 'Numero de Transacciones (Millones)',
			'titlefont' : dict(size=30),
			'tickfont' : dict(size=20)
	    },
	    'yaxis2': {
	    	'title' : 'Precio Bitcoin ($)',
			'titlefont' : dict(size=30, color='rgb(203, 50, 52)'),
			'tickfont' : dict(size=20, color='rgb(203, 50, 52)'),
	        'overlaying' : 'y',
        	'side' : 'right'
	    }
	}
	fig = {
	    'data': [traza2, traza3, traza1],
	    'layout': layout,
	}
	plotly.offline.plot(fig,filename='diagramas/opreturn/transacciones_precio_tiempo.html', auto_open=True)	

if __name__ == '__main__':
  main()
