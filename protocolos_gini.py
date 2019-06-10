import sys
import os
import plotly 
import plotly.graph_objs as go

def main():
	"""Programa para generar los diagramas de los protocolos de Bitcoin respecto al numero de txs y el tamano 
	y asi calcular sus coeficientes de Gini, segun el caso que el usuario pida por argumento de entrada"""
	
	# Comprobamos que argumento nos pasan por parametro para usar uno u otro archivo de datos
	if len(sys.argv) == 1 or len(sys.argv) > 2:
		print 'Ejecuta el programa con uno de estos argumentos: txs o tamano'
		sys.exit()
	elif sys.argv[1] == 'txs':
		archivo_entrada = 'protocolos_TXs.data'
		archivo_salida = 'txs'
	elif sys.argv[1] == 'tamano':
		archivo_entrada = 'protocolos_Tamano.data'
		archivo_salida = 'tamano'
	else:
		sys.exit()

	# Inicializo algunas variables que utilizare despues
	i = 0
	txs_tamano_totales = 0
	nombres = []
	txs_tamano = []
	acumula_nombres = []
	acumula_txs_tamano = []
	
	# Los datos que parseo los he obtenido de los programas protocolos_categorias.py  y protocolos_categorias_sin_desc.py
	with open('data/' + archivo_entrada) as f:
		while True:
			line = f.readline()
			# Longitud cero indica final de fichero
			if len(line) == 0:
				break
			#Partimos la linea y guardamos el nombre y su numero de txs o tamano
			lista = line.split()
			nombres.append(lista[0])
			txs_tamano.append(int(lista[1]))
			txs_tamano_totales = txs_tamano_totales + int(lista[1])
	f.close()  

	# Revertimos las listas para dibujar mejor el % acumulado de txs o tamano respecto al % acumulado de lo que se nos
	# pida por comandos
	# Asi podremos observar si hay descentralizacion en el diagrama
	nombres_reverse = nombres[::-1]
	txs_tamano_reverse = txs_tamano[::-1]

	# Ahora hallo el porcentaje acumulado de los protocolos y el porcentaje acumulado del argumento pasado por comandos
	while i < len(nombres):
		# Inicializacion primer termino
		if i == 0:
			acumula_nombres.append(1.0/len(nombres))
			acumula_txs_tamano.append(txs_tamano_reverse[i]*1.0/txs_tamano_totales)
			coef_nombres_txs_tamano = 0
		# Resto de terminos y calculo del coeficiente de Gini segun la formula conocida
		else:
			acumula_nombres.append(acumula_nombres[i-1] + 1.0/len(nombres))
			acumula_txs_tamano.append(acumula_txs_tamano[i-1] + txs_tamano_reverse[i]*1.0/txs_tamano_totales)
			coef_nombres_txs_tamano = coef_nombres_txs_tamano + ((acumula_nombres[i] - acumula_nombres[i-1])*(acumula_txs_tamano[i] + acumula_txs_tamano[i-1]))
		i= i+1

	# Segun la opcion que haya elegido el usuario, se imprimiran unos datos u otros
	if sys.argv[1] == 'txs':
		print 'Coeficiente de  Gini de Protocolos - #TXs:', abs(1 - coef_nombres_txs_tamano)
	elif sys.argv[1] == 'tamano':
		print 'Coeficiente de  Gini de Protocolos - Tamano TXs:', abs(1 - coef_nombres_txs_tamano)
	
	# DIAGRAMA DE BARRAS %ACUMULADO PROTOCOLOS RESPECTO AL %ACUMULADO DE LO QUE SE PIDA POR COMANDOS
	traza = go.Bar(x=acumula_nombres, y=acumula_txs_tamano,  hoverinfo='x+y')
	layout = {
		'xaxis': {
			'title' : 'Porcentaje acumulado de Protocolos',
	    	'tickformat': ',.0%',
    		'range': [0,1.1]
	    },
	    'yaxis': {
	    	'title' : 'Porcentaje acumulado de '+archivo_salida,
	    	'tickformat': ',.0%',
	        'range': [0, 1.1]
	    },
	    'shapes': [
	        # Linea Horizontal que marca del 50% de hashrate acumulado
	        {
	            'type': 'line',
	            'x0': 0,
	            'y0': 0.5,
	            'x1': 1,
	            'y1': 0.5,
	            'line': {
	                'color': 'rgb(50, 171, 96)',
	                'width': 2.5,
	            },
	        },
	        # Linea Vertical que marca el 50% de pools acumulado
	        {
	            'type': 'line',
	            'x0': 0.5,
	            'y0': 0,
	            'x1': 0.5,
	            'y1': 1,
	            'line': {
	                'color': 'rgb(50, 171, 96)',
	                'width': 2.5,
	            },
	        }
	    ]
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	# Dibujo el diagrama de lineas ayudandome de la libreria plotly
	plotly.offline.plot(fig,filename='diagramas/descentralizacion/protocolos_gini_'+archivo_salida+'_descenc.html', auto_open=True)	
	
if __name__ == '__main__':
  main()
