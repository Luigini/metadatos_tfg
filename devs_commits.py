import os
import plotly 
import plotly.graph_objs as go

def main():
	"""Programa para generar los diagramas de los desarrolladores de Bitcoin Core respecto
	al numero de commits realizados para ese cliente y calcular su coeficientes de Gini"""
	
	# Inicializo algunas variables que utilizare despues
	i = 0
	commits_totales = 0
	nombres_contribuidores = []
	numero_commits = []
	acumula_contribuidores = []
	acumula_commits = []
	
	# Los datos que he parseado los he obtenido desde la web https://bitcoin.org/en/development#dev-communities
	with open('/home/donvito/Escritorio/metadatos/data/devs_commits.data') as f:
		while True:
			line = f.readline()
			# Longitud cero indica final de fichero
			if len(line) == 0:
				break
			#Partimos la linea y guardamos el nombre del desarrollador y el numero de commits que ha realizado
			lista = line.split()
			nombres_contribuidores.append(lista[0])
			numero_commits.append(int(lista[1]))
			commits_totales = commits_totales + int(lista[1])

	f.close()  

	print 'Numero de desarrolladores:', len(nombres_contribuidores)
	print 'Commits Totales:', commits_totales

	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = '/home/donvito/Escritorio/metadatos/diagramas/descentralizacion'
	if not os.path.exists(dir):
		os.mkdir(dir)

	# Revertimos las listas para dibujar mejor el % acumulado de desarrolladores respecto al % acumulado de commits
	# Asi podremos observar si hay descentralizacion en el diagrama
	nombres_contribuidores_reverse = nombres_contribuidores[::-1]
	numero_commits_reverse = numero_commits[::-1]

	# DIAGRAMA CIRCULAR DESARROLLADOR - COMMITS
	data = go.Pie(labels=nombres_contribuidores, values=numero_commits, hoverinfo='label+value', textinfo='label+percent')
	plotly.offline.plot({
		"data": [data],
		"layout": go.Layout(title="Desarrolladores/Porcentaje de Commits (Desde 2009)", autosize=True)
		},filename='diagramas/descentralizacion/devs_commits.html', auto_open=True)	

	# DIAGRAMA CIRCULAR TOP 25 DESARROLLADOR - COMMITS
	data = go.Bar(x=nombres_contribuidores[0:24], y=numero_commits[0:24], hoverinfo='x+y')
	plotly.offline.plot({
		"data": [data],
		"layout": go.Layout(title="Top 25 Desarrolladores/Numero Commits (Desde 2009)", autosize=True)
		},filename='diagramas/descentralizacion/devs_commits_top25.html', auto_open=True)	

	# Ahora hallo el porcentaje acumulado en el numero de desarrolladores y el porcentaje acumulado de commits
	while i < len(nombres_contribuidores):
		# Inicializacion primer termino
		if i == 0:
			acumula_contribuidores.append(1.0/len(nombres_contribuidores))
			acumula_commits.append(numero_commits_reverse[i]*1.0/commits_totales)
			coeficiente = 0
		# Resto de terminos y calculo del coeficiente de Gini segun la formula conocida
		else:
			acumula_contribuidores.append(acumula_contribuidores[i-1] + 1.0/len(nombres_contribuidores))
			acumula_commits.append(acumula_commits[i-1] + numero_commits_reverse[i]*1.0/commits_totales)
			coeficiente = coeficiente + ((acumula_contribuidores[i] - acumula_contribuidores[i-1])*(acumula_commits[i] + acumula_commits [i-1]))
		i= i+1

	print 'Coeficiente de  Gini de Desarrolladores - Commits:', abs(1 - coeficiente)

	# DIAGRAMA DE BARRAS %ACUMULADO NUMERO DESARROLLADORES - %ACUMULADO NUMERO COMMITS
	traza = go.Bar(x=acumula_contribuidores, y=acumula_commits, hoverinfo='x+y')
	layout = {
		'xaxis': {
			'title' : 'Porcentaje acumulado de Desarrolladores de Bitcoin Core',
	    	'tickformat': ',.0%',
    		'range': [0,1.1]
	    },
	    'yaxis': {
	    	'title' : 'Porcentaje acumulado de Commits',
	    	'tickformat': ',.0%',
	        'range': [0, 1.1]
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
	        }
	    ]
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	# Dibujo el diagrama de lineas ayudandome de la libreria plotly
	plotly.offline.plot(fig,filename='diagramas/descentralizacion/devs_commits_descentral.html', auto_open=True)	

if __name__ == '__main__':
  main()
