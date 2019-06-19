import sys
import os
import plotly 
import plotly.graph_objs as go

def main():
	"""Programa para generar los diagramas de los nodos publicos (y alcanzables) de Bitcoin respecto al 
	cliente que usan, el pais en el que se encuentran y la red en la que operan. 
	Ademas, calculamos sus coeficientes de Gini"""
	
	# Comprobamos que argumento nos pasan por parametro para usar uno u otro archivo de datos
	if len(sys.argv) == 1 or len(sys.argv) > 2:
		print 'Ejecuta el programa con uno de estos argumentos: cliente, cliente_unificados, pais o red'
		sys.exit()
	elif sys.argv[1] == 'cliente':
		archivo_entrada = 'nodos_por_cliente.data'
		archivo_salida = 'cliente'
	elif sys.argv[1] == 'cliente_unificados':
		archivo_entrada = 'nodos_por_cliente_unificados.data'
		archivo_salida = 'cliente_unificados'
	elif sys.argv[1] == 'pais':
		archivo_entrada = 'nodos_por_pais.data'
		archivo_salida = 'pais'
	elif sys.argv[1] == 'red':
		archivo_entrada = 'nodos_por_red.data'
		archivo_salida = 'red'
	else:
		sys.exit()

	# Inicializo algunas variables que utilizare despues
	i = 0
	nodos_totales = 0
	nombres = []
	nodos = []
	acumula_nombres = []
	acumula_nodos = []
	
	# Los datos que he parseado los he obtenido desde la web https://bitnodes.earn.com/nodes/
	# El sabado 8 de Junio a las 14:00:10
	with open('data/' + archivo_entrada) as f:
		while True:
			line = f.readline()
			# Longitud cero indica final de fichero
			if len(line) == 0:
				break
			#Partimos la linea y guardamos el nombre y su numero de nodos
			lista = line.split()
			nombres.append(lista[0])
			nodos.append(int(lista[1]))
			nodos_totales = nodos_totales + int(lista[1])
	f.close()  

	# Segun la opcion que haya elegido el usuario, se imprimiran unos datos u otros
	if sys.argv[1] == 'cliente':
		print 'Numero de clientes en Bitcoin el 8 de Junio a las 14:00:10:', len(nombres)
	elif sys.argv[1] == 'cliente_unificados':
		print 'Numero de clientes (unificados) en Bitcoin el 8 de Junio a las 14:00:10:', len(nombres)
	elif sys.argv[1] == 'pais':
		print 'Numero de paises en Bitcoin el 8 de Junio a las 14:00:10:', len(nombres)
	elif sys.argv[1] == 'red':	
		print 'Numero de redes en Bitcoin el 8 de Junio a las 14:00:10:', len(nombres)

	print 'Numero total de Nodos publicos (alcanzables) en Bitcoin:', nodos_totales

	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = 'diagramas'
	if not os.path.exists(dir):
		os.mkdir(dir)
	if not os.path.exists('diagramas/descentralizacion'):
		os.mkdir('diagramas/descentralizacion')
	if not os.path.exists('diagramas/descentralizacion/anexos'):
		os.mkdir('diagramas/descentralizacion/anexos')		


	# DIAGRAMA CIRCULAR NODOS RESPECTO A LO QUE SE PIDA POR COMANDOS
	data = go.Pie(labels=nombres, values=nodos, textfont=dict(size=18), hoverinfo='label+value', textinfo='label+percent')
	plotly.offline.plot({
		"data": [data],
		"layout": go.Layout(title="Nodos por "+archivo_salida, font = dict(size=20), autosize=True)
	},filename='diagramas/descentralizacion/nodos_por_'+archivo_salida+'.html', auto_open=True)	

	# Revertimos las listas para dibujar mejor el % acumulado de nodos respecto al % acumulado de lo que se nos
	# pida por comandos
	# Asi podremos observar si hay descentralizacion en el diagrama
	nombres_reverse = nombres[::-1]
	nodos_reverse = nodos[::-1]

	# Ahora hallo el porcentaje acumulado en el numero de nodos y el porcentaje acumulado del argumento pasado por comandos
	while i < len(nombres):
		# Inicializacion primer termino
		if i == 0:
			acumula_nombres.append(1.0/len(nombres))
			acumula_nodos.append(nodos_reverse[i]*1.0/nodos_totales)
			coef_nombres_nodos = 0
		# Resto de terminos y calculo del coeficiente de Gini segun la formula conocida
		else:
			acumula_nombres.append(acumula_nombres[i-1] + 1.0/len(nombres))
			acumula_nodos.append(acumula_nodos[i-1] + nodos_reverse[i]*1.0/nodos_totales)
			coef_nombres_nodos = coef_nombres_nodos + ((acumula_nombres[i] - acumula_nombres[i-1])*(acumula_nodos[i] + acumula_nodos [i-1]))
		i= i+1

	# Segun la opcion que haya elegido el usuario, se imprimiran unos datos u otros
	if sys.argv[1] == 'cliente':
		print 'Coeficiente de  Gini de Clientes - Nodos:', abs(1 - coef_nombres_nodos)
	elif sys.argv[1] == 'cliente_unificados':
		print 'Coeficiente de  Gini de Clientes (Unificados) - Nodos:', abs(1 - coef_nombres_nodos)	
	elif sys.argv[1] == 'pais':
		print 'Coeficiente de  Gini de Paises - Nodos:', abs(1 - coef_nombres_nodos)
	elif sys.argv[1] == 'red':	
		print 'Coeficiente de  Gini de Redes - Nodos:', abs(1 - coef_nombres_nodos)
	
	# DIAGRAMA DE BARRAS %ACUMULADO NODOS RESPECTO AL %ACUMULADO DE LO QUE SE PIDA POR COMANDOS
	traza = go.Bar(x=acumula_nombres, y=acumula_nodos,  hoverinfo='x+y')
	layout = {
		'title' : { 
			'text' : "Coeficiente de Gini: " + str(abs(1 - coef_nombres_nodos)),
			'font' : dict(size=25)
		},
		'xaxis': {
			'title' : 'Porcentaje acumulado de '+archivo_salida,
	    	'tickformat': ',.0%',
    		'range': [0,1.1],
    		'titlefont' : dict(size=25),
			'tickfont' : dict(size=20),
	    },
	    'yaxis': {
	    	'title' : 'Porcentaje acumulado de Nodos',
	    	'tickformat': ',.0%',
	        'range': [0, 1.1],
    		'titlefont' : dict(size=25),
			'tickfont' : dict(size=20),
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
	        },
	       	# Linea Diagonal que marca la curva de lorenz de completa igualdad
	        {
	            'type': 'line',
	            'x0': 0,
	            'y0': 0,
	            'x1': 1,
	            'y1': 1,
	            'line': {
	                'color': 'rgb(203, 50, 52)',
	                'width': 3.5,
	            },
	        },
	    ]
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	# Dibujo el diagrama de lineas ayudandome de la libreria plotly
	plotly.offline.plot(fig,filename='diagramas/descentralizacion/nodos_por_'+archivo_salida+'_descenc.html', auto_open=True)	
	
if __name__ == '__main__':
  main()
