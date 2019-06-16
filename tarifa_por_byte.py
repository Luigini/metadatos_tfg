import os
import json
import datetime
import plotly
import plotly.graph_objs as go

def main():
	"""Programa que realiza varios calculos y genera varios diagramas:
	- Estudio del coste economico de las TXs OP_RETURN. Los datos de las comisiones de las OP_RETURN TXs obtenidas 
	por los mineros cada mes los he extraido de la web https://opreturn.org/op-return-per-month/ tras haber 
	comprobado su validez
	- Generacion de un grafico lineal del total acumulado de comisiones por mes
	- Generacion de un diagrama de barras con el numero de TXs por cada tamano medio de TX"""
	
	# Lugar del que obtenemos las transacciones OP_RETURN en bruto
	dir = 'archivos_formateados/'

	# Variables inicializadas que usare
	inicio = 0
	final =  578704 #578703
	total_op_returns = 0;
	total_comisiones = 0
	total_bytes_TXs = 0;
	fechas = []
	eje_x = []
	comisiones = [0.225,0.005,0.0024,0.0145,0.0066638,0.00876165,0.02903776,0.0039643,0.00575246,0.0360116,0.01348378,
				0.00881961,0.14088718,0.06445304,0.11308584,0.10477768,0.20972309,0.19240893,0.20153741,0.29673085,
				0.64115276,0.36368834,0.40577751,0.8250739,1.03641455,1.03126657,6.55469483,2.27132574,20.69744589,
				5.05575053,7.14959554,6.02552417,5.37579135,11.03938767,14.88966974,15.1786119,11.60543435,13.43618449,
				14.76016496,21.37710214,19.97873842,21.63527145,19.85996811,26.92735736,34.32799541,35.48554465,85.77529698,
				99.17773579,135.30867159,140.74330128,91.38029291,123.9351614,95.45808639,71.51802917,175.00399826,409.73842431,
				346.38588251,92.8148477,44.36139868,38.26035948,34.76127815,53.62683495,41.92202167,35.72748492,33.90319522,
				38.94740792,62.41114455,63.6199754,73.29820142,72.54856334,130.42389894,426.95476222,730.7238385];

	tamano_TX_medio = {}

	# Hallamos el numero acumulado de comisiones  por mes desde el principio de los tiempo
	for  comision_mes in comisiones:
		total_comisiones = total_comisiones + comision_mes

	# Cargar contenido archivos para obtener la lista de meses donde se acumularon las comisiones
	for i in range (inicio,final):
		with open(dir + str(i) + '.json') as f:
			datos = json.load(f)
			
			# Tomo la marca de tiempo de los bloques en los que haya TXs OP_RETURN
			timestamp = datos['timestamp']
			if timestamp:
				# Transformo la fecha y la formateo extrayendo el anyo y el mes
				fecha = datetime.datetime.fromtimestamp(float(timestamp)).isoformat()
				fecha_formateada = int(fecha[:4] + fecha[6:7])
				if fecha_formateada not in fechas:
					fechas.append(fecha_formateada)

			# Bloque CON TXs OP_RETURN	
			if datos['op_returns'] != []:	   
				 
				# Obtenemos el total de TXs OP_RETURN
				total_op_returns = total_op_returns + len(datos['op_returns'])

				for transaccion in datos['op_returns']:
					# El tamano en bytes de una transaccion OP_RETURN se halla tomando un byte por cada digito hexadecimal
					bytes_transaccion = len(transaccion['hex'])*1.0/2
					total_bytes_TXs = total_bytes_TXs + bytes_transaccion
					
					# Cuento el numero de TXs de cada tamano medio para dibuja despues una grafica compartiva
					if bytes_transaccion not in tamano_TX_medio:
						tamano_TX_medio [bytes_transaccion] = 1
					else:
						tamano_TX_medio [bytes_transaccion] = tamano_TX_medio [bytes_transaccion] + 1

			#print i

		f.close() 

	# Si la carpeta no esta creada, genero la carpeta donde se almacenaran los graficos producidos por el programa
	dir = 'diagramas'
	if not os.path.exists(dir):
		os.mkdir(dir)
	if not os.path.exists('diagramas/opreturn'):
		os.mkdir('diagramas/opreturn')

	# Imprimimos la informacion que necesitamos
	print 'Total acumulado de las comisiones: {0:.4f}'.format(total_comisiones), 'BTC'
	print '#TXs OP_RETURN:', total_op_returns, 'TXs'
	print 'Tamano total en bytes de las TXs OP_RETURN:', total_bytes_TXs, 'bytes'
	print 'Coste medio por transaccion:', total_comisiones/total_op_returns, 'BTC/TX'
	print 'Tamano medio de una TX OP_RETURN en bytes: {0:.4f}'.format(total_bytes_TXs/total_op_returns), 'bytes/TX'
	print 'Coste (Comision) medio de almacenamiento por byte:', (total_comisiones/total_op_returns) / (total_bytes_TXs/total_op_returns), 'BTC/byte'

	# GRAFICO LINEAL MESES-TOTAL COMISIONES
	# Dibujo el diagrama de barras ayudandome de la libreria plotly
	for i in range(len(comisiones)):
		eje_x.append(i)
	traza = go.Scatter(x=eje_x, y=comisiones, mode='lines+markers', hoverinfo='y')
	layout = {
		'title' : { 
			'text' : "Comisiones (BTC) en el tiempo",
			'font' : dict(size=40)
		},
		'xaxis': {
			'tickfont' : dict(size=25),
        	'tickmode' : 'array',
       		'tickvals' : [0, 8, 19, 31, 43, 55, 67, 72],
        	'ticktext' : ['03-2013','2014','2015','2016','2017','2018','2019','05-2019']
	    },
	    'yaxis': {
	    	'title' : 'Comisiones (BTC)',
			'titlefont' : dict(size=30),
			'tickfont' : dict(size=20)
	    }
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	plotly.offline.plot(fig,filename='diagramas/opreturn/comisiones_por_mes.html', auto_open=True)	



	# Dibujo el diagrama lineal ayudandome de la libreria plotly
	# GRAFICO DE BARRAS TAMANO MEDIO - #TXs
	# Ordeno el diccionario por tamano medio de transaccion
	tamano_TX_medio_ordenada = sorted(tamano_TX_medio.items())
	tamanos = []
	num_TXs = []

	# Convertimos la estructura diccionario en listas para dibujar el grafico
	for tamano, numero in tamano_TX_medio_ordenada:
		tamanos.append(tamano)
		num_TXs.append(numero)
	
	# Dibujo el diagrama de barras ayudandome de la libreria plotly
	traza = go.Bar(x=tamanos, y=num_TXs, hoverinfo='x+y')
	layout = {
		'title' : { 
			'text' : 'Tamano Medio de TX(bytes) / Numero TXs',
			'font' : dict(size=40)
		},
		'xaxis': {
			'title' : 'Tamano Medio de TX(bytes)',
			'titlefont' : dict(size=30),
			'tickfont' : dict(size=25)
	    },
	    'yaxis': {
	    	'title' : 'Numero TXs',
			'titlefont' : dict(size=30),
			'tickfont' : dict(size=25)
	    }
	}
	fig = {
	    'data': [traza],
	    'layout': layout,
	}
	plotly.offline.plot(fig,filename='diagramas/opreturn/tamano_TX_medio.html', auto_open=True)	

	#plotly.offline.plot({
	#	"data": [go.Bar(x=tamanos, y=num_TXs, hoverinfo='x+y')],
	#	"layout": go.Layout(title="Numero TXs / Tamano Medio de TX", autosize=True,
	#		 xaxis=go.layout.XAxis(tickvals=tamanos))
	#	},filename='diagramas/opreturn/tamano_TX_medio.html', auto_open=True, )	



if __name__ == '__main__':
  main()
