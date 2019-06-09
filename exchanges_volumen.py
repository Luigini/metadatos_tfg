import sys
import os
import plotly 
import plotly.graph_objs as go

def main():
	"""Programa para generar los diagramas de los exchanges que operan en Bitcoin con el
	volumen de bitcoins que mueven"""
	
	# Comprobamos que argumento nos pasan por parametro para usar uno u otro archivo de datos
	if len(sys.argv) == 1 or len(sys.argv) > 2:
		print 'Ejecuta el programa con uno de estos argumentos: 1d, 1m, 5y'
		sys.exit()
	elif sys.argv[1] == '1d':
		archivo_entrada = 'exchanges_volumen_1d.data'
		archivo_salida = '_1d'
	elif sys.argv[1] == '1m':
		archivo_entrada = 'exchanges_volumen_1m.data'
		archivo_salida = '_1m'
	elif sys.argv[1] == '2y':
		archivo_entrada = 'exchanges_volumen_2y.data'
		archivo_salida = '_2y'
	else:
		sys.exit()

	# Inicializo algunas variables que utilizare despues
	i = 0
	volumen_total = 0	
	nombres_exchanges = []
	volumen = []
	acumula_exchanges = []
	acumula_volumen = []
	
	# Los datos que he parseado los he obtenido desde la web https://data.bitcoinity.org/markets/exchanges/USD/30d
	with open('/home/donvito/Escritorio/metadatos/data/' + archivo_entrada) as f:
		while True:
			line = f.readline()
			# Longitud cero indica final de fichero
			if len(line) == 0:
				break
			#Partimos la linea y guardamos el nombre del exchange y su volumen
			lista = line.split()
			nombres_exchanges.append(lista[0])
			volumen.append(int(lista[1]))
			volumen_total = volumen_total + int(lista[1])

	f.close()  

	print 'Numero de exchanges:', len(nombres_exchanges)
	print 'Volumen Total (BTC):', volumen_total 

	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = '/home/donvito/Escritorio/metadatos/diagramas/descentralizacion'
	if not os.path.exists(dir):
		os.mkdir(dir)

	# DIAGRAMA CIRCULAR EXCHANGES - VOLUMEN
	plotly.offline.plot({
		"data": [go.Pie(labels=nombres_exchanges, values=volumen, hoverinfo='label+value', textinfo='label+percent')],
		"layout": go.Layout(title="Exchanges/Volumen (BTC)")
		},filename='diagramas/descentralizacion/exchanges_volumen'+archivo_salida+'.html', auto_open=True)

	# Revertimos las listas para dibujar mejor el % acumulado de exchanges respecto al % acumulado de volumen
	# Asi podremos observar si hay descentralizacion en el diagrama
	nombres_exchanges_reverse = nombres_exchanges[::-1]
	volumen_reverse = volumen[::-1]

	# Ahora hallo el porcentaje acumulado en el numero de exchanges y el porcentaje acumulado de volumen en bitcoins
	while i < len(nombres_exchanges):
		# Inicializacion primer termino
		if i == 0:
			acumula_exchanges.append(1.0/len(nombres_exchanges))
			acumula_volumen.append(volumen_reverse[i]*1.0/volumen_total)
			coef_exchanges_volumen = 0
		# Resto de terminos y calculo del coeficiente de Gini segun la formula conocida
		else:
			acumula_exchanges.append(acumula_exchanges[i-1] + 1.0/len(nombres_exchanges))
			acumula_volumen.append(acumula_volumen[i-1] + volumen_reverse[i]*1.0/volumen_total)
			coef_exchanges_volumen = coef_exchanges_volumen + ((acumula_exchanges[i] - acumula_exchanges[i-1])*(acumula_volumen[i] + acumula_volumen [i-1]))
		i= i+1

	print 'Coeficiente de  Gini de Exchanges - Volumen:', abs(1 - coef_exchanges_volumen)

	# DIAGRAMA LINEAL %ACUMULADO NUMERO EXCHANGES - %ACUMULADO DE VOLUMEN
	traza = go.Bar(x=acumula_exchanges, y=acumula_volumen, hoverinfo='x+y')
	layout = {
		'xaxis': {
			'title' : 'Porcentaje acumulado de exchanges de Bitcoin',
	    	'tickformat': ',.0%',
    		'range': [0,1.1]
	    },
	    'yaxis': {
	    	'title' : 'Porcentaje de Volumen (BTC) acumulado',
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
	plotly.offline.plot(fig,filename='diagramas/descentralizacion/exchanges_volumen'+archivo_salida+'_descentral.html', auto_open=True,)	
	
if __name__ == '__main__':
  main()
