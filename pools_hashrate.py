import sys
import os
import plotly 
import plotly.graph_objs as go

def main():
	"""Programa para generar los diagramas de los pools que operan en Bitcoin respecto
	a su hashrate y calcular sus coeficiente de Gini"""
	
	# Comprobamos que argumento nos pasan por parametro para usar uno u otro archivo de datos
	if len(sys.argv) == 1 or len(sys.argv) > 2:
		print 'Ejecuta el programa con uno de estos argumentos: 1d, 1m, 1y, all'
		sys.exit()
	elif sys.argv[1] == '1d':
		archivo_entrada = 'pools_hashrate_bloques_1d.data'
		archivo_salida = '_1d'
	elif sys.argv[1] == '1m':
		archivo_entrada = 'pools_hashrate_bloques_1m.data'
		archivo_salida = '_1m'
	elif sys.argv[1] == '1y':
		archivo_entrada = 'pools_hashrate_bloques_1y.data'
		archivo_salida = '_1y'
	elif sys.argv[1] == 'all':
		archivo_entrada = 'pools_hashrate_bloques_all.data'
		archivo_salida = '_all'
	else:
		sys.exit()

	# Inicializo algunas variables que utilizare despues
	i = 0
	hashrate_total = 0
	bloques_minados_total = 0
	nombres_pools = []
	hashrate = []
	bloques_minados = []
	acumula_pools = []
	acumula_hashrate = []
	acumula_bloques_minados = []
	
	# Los datos que he parseado los he obtenido desde la web https://btc.com/stats/pool
	with open('data/' + archivo_entrada) as f:
		while True:
			line = f.readline()
			# Longitud cero indica final de fichero
			if len(line) == 0:
				break
			#Partimos la linea y guardamos el nombre del pool y su hashrate
			lista = line.split()
			nombres_pools.append(lista[0])
			hashrate.append(float(lista[1]))
			hashrate_total = hashrate_total + float(lista[1])
			bloques_minados.append(int(lista[2]))
			bloques_minados_total = bloques_minados_total + int(lista[2])		

	f.close()  

	print 'Numero de pools:', len(nombres_pools)
	print 'Numero de bloques minados:', bloques_minados_total

	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = 'diagramas'
	if not os.path.exists(dir):
		os.mkdir(dir)
	if not os.path.exists('diagramas/descentralizacion'):
		os.mkdir('diagramas/descentralizacion')

	# DIAGRAMA CIRCULAR POOLS - HASHRATE
	data = go.Pie(labels=nombres_pools, values=hashrate, hoverinfo='label+value', textinfo='label+percent')
	plotly.offline.plot({
		"data": [data],
		"layout": go.Layout(title="Pools/Hashrate (hash/s)", autosize=True)
		},filename='diagramas/descentralizacion/pools_hashrate'+archivo_salida+'.html', auto_open=True)	

	# DIAGRAMA CIRCULAR POOLS - BLOQUES MINADORS
	data = go.Pie(labels=nombres_pools, values=bloques_minados, hoverinfo='label+value', textinfo='label+percent')
	plotly.offline.plot({
		"data": [data],
		"layout": go.Layout(title="Pools/Bloques Minados", autosize=True)
		},filename='diagramas/descentralizacion/pools_bloques_minados'+archivo_salida+'.html', auto_open=True)	

	# Revertimos las listas para dibujar mejor el % acumulado de pools respecto % acumulado de hashrate y
	# respecto % acumulado de bloques minados aparte
	# Asi podremos observar si hay descentralizacion en el diagrama
	nombres_pools_reverse = nombres_pools[::-1]
	hashrate_reverse = hashrate[::-1]
	bloques_minados_reverse = bloques_minados[::-1]

	# Ahora hallo el porcentaje acumulado en el numero de pools y el porcentaje acumulado de hasrate y bloques minados
	while i < len(nombres_pools):
		# Inicializacion primer termino
		if i == 0:
			acumula_pools.append(1.0/len(nombres_pools))
			acumula_hashrate.append(hashrate_reverse[i]*1.0/hashrate_total)
			acumula_bloques_minados.append(bloques_minados_reverse[i]*1.0/bloques_minados_total)
			coef_pools_hashrate = 0
			coef_pools_bloques_minados = 0
		# Resto de terminos y calculo del coeficiente de Gini segun la formula conocida
		else:
			acumula_pools.append(acumula_pools[i-1] + 1.0/len(nombres_pools))
			acumula_hashrate.append(acumula_hashrate[i-1] + hashrate_reverse[i]*1.0/hashrate_total)
			coef_pools_hashrate = coef_pools_hashrate + ((acumula_pools[i] - acumula_pools[i-1])*(acumula_hashrate[i] + acumula_hashrate [i-1]))
			
			acumula_bloques_minados.append(acumula_bloques_minados[i-1] + bloques_minados_reverse[i]*1.0/bloques_minados_total)
			coef_pools_bloques_minados = coef_pools_bloques_minados + ((acumula_pools[i] - acumula_pools[i-1])*(acumula_bloques_minados[i] + acumula_bloques_minados [i-1]))
		i= i+1

	print 'Coeficiente de  Gini de Pools - HashRate:', abs(1 - coef_pools_hashrate)
	print 'Coeficiente de  Gini de Pools - Bloques Minados:', abs(1 - coef_pools_bloques_minados)
	
	# DIAGRAMA DE BARRAS %ACUMULADO NUMERO POOLS - %ACUMULADO DE HASHRATE
	traza = go.Bar(x=acumula_pools, y=acumula_hashrate,  hoverinfo='x+y')
	layout = {
		'xaxis': {
			'title' : 'Porcentaje acumulado de Pools de Bitcoin',
	    	'tickformat': ',.0%',
    		'range': [0,1.1]
	    },
	    'yaxis': {
	    	'title' : 'Porcentaje acumulado de Hashrate',
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
	plotly.offline.plot(fig,filename='diagramas/descentralizacion/pools_hashrate'+archivo_salida+'_descenc.html', auto_open=True)	
	
	# DIAGRAMA DE BARRAS %ACUMULADO NUMERO POOLS - %ACUMULADO DE BLOQUES MINADOS
	traza = go.Bar(x=acumula_pools, y=acumula_bloques_minados,  hoverinfo='x+y')
	layout = {
		'xaxis': {
			'title' : 'Porcentaje acumulado de Pools de Bitcoin',
	    	'tickformat': ',.0%',
    		'range': [0,1.1]
	    },
	    'yaxis': {
	    	'title' : 'Porcentaje acumulado de Bloques Minados ',
	    	'tickformat': ',.0%',
	        'range': [0, 1.1]
	    },
	    'shapes': [
	        # Linea Horizontal que marca del 50% de bloques minados acumulado
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
	plotly.offline.plot(fig,filename='diagramas/descentralizacion/pools_bloques_minados'+archivo_salida+'_descentral.html', auto_open=True)	

if __name__ == '__main__':
  main()
