import os
import plotly 
import plotly.graph_objs as go

def main():
	"""Programa para generar el diagrama de barra de las diracciones anonimas de Bitcoin Core respecto
	al numero de bitcoins que contienen sus saldos y asi calcular despues su coeficientes de Gini"""
	
	# Inicializo algunas variables que utilizare despues
	i = 0
	direcciones = []
	acumula_direcciones = []
	bitcoins = []		
	numero_bitcoins = 0
	acumula_bitcoins = []
	
	# Los datos que he parseado los he obtenido desde la web https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html
	with open('data/top_350direcciones_5000bitcoins.data') as f:
		while True:
			line = f.readline()
			# Longitud cero indica final de fichero
			if len(line) == 0:
				break
			#Partimos la linea y guardamos el intervalo del balance, el numero de direcciones y el numero
			#de bitcoins contenidos en cada balance
			lista = line.split()
			direcciones.append(lista[0])
			bitcoins.append(int(lista[1]))
			numero_bitcoins = numero_bitcoins + int(lista[1])
			
	f.close()  

	print 'Numero total de direcciones:', len(direcciones)
	print 'Numero total de bitcoins:', numero_bitcoins

	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = 'diagramas'
	if not os.path.exists(dir):
		os.mkdir(dir)
	if not os.path.exists('diagramas/descentralizacion'):
		os.mkdir('diagramas/descentralizacion')
	if not os.path.exists('diagramas/descentralizacion/anexos'):
		os.mkdir('diagramas/descentralizacion/anexos')		

	# Revertimos las listas para dibujar mejor el % acumulado de direcciones respecto al % acumulado de bitcoins
	# Asi podremos observar si hay descentralizacion en el diagrama
	direcciones_reverse = direcciones[::-1]
	bitcoins_reverse = bitcoins[::-1]

	# Ahora hallo el porcentaje acumulado del numero de direcciones y el porcentaje acumulado del numero de bitcoins
	while i < len(direcciones):
		# Inicializacion primer termino
		if i == 0:
			acumula_direcciones.append(1.0/len(direcciones))
			acumula_bitcoins.append(bitcoins_reverse[i]*1.0/numero_bitcoins)
			coeficiente = 0
		# Resto de terminos y calculo del coeficiente de Gini segun la formula conocida
		else:
			acumula_direcciones.append(acumula_direcciones[i-1] + 1.0/len(direcciones))
			acumula_bitcoins.append(acumula_bitcoins[i-1] + bitcoins_reverse[i]*1.0/numero_bitcoins)
			coeficiente = coeficiente + ((acumula_direcciones[i] - acumula_direcciones[i-1])*(acumula_bitcoins[i] + acumula_bitcoins [i-1]))
		i= i+1

	print 'Coeficiente de  Gini de Direcciones - Bitcoins:', abs(1 - coeficiente)

	# DIAGRAMA DE BARRAS %ACUMULADO NUMERO DIRECCIONES - %ACUMULADO NUMERO BITCOINS
	traza = go.Bar(x=acumula_direcciones, y=acumula_bitcoins, hoverinfo='x+y')
	layout = {
		'title' : { 
			'text' : "Coeficiente de Gini: " + str(abs(1 - coeficiente)),
			'font' : dict(size=25)
		},
		'xaxis': {
			'title' : 'Porcentaje acumulado de Direcciones Bitcoin',
	    	'tickformat': ',.0%',
    		'range': [0,1.1],
    		'titlefont' : dict(size=25),
			'tickfont' : dict(size=20),
	    },
	    'yaxis': {
	    	'title' : 'Porcentaje acumulado de bitcoins',
	    	'tickformat': ',.0%',
	        'range': [0, 1.1],
    		'titlefont' : dict(size=25),
			'tickfont' : dict(size=20),
	    },
	    'shapes': [
	        # Linea Horizontal que marca del 50% de commits acumulado
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
	        # Linea Vertical que marca el 50% de desarrolladores acumulado
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
	        }
	    ]
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	# Dibujo el diagrama de lineas ayudandome de la libreria plotly
	plotly.offline.plot(fig,filename='diagramas/descentralizacion/top_direcciones_propiedades.html', auto_open=True)	

if __name__ == '__main__':
  main()
