# Estudio de metadatos de la cadena de bloques de Bitcoin 

_Las tecnologías de blockchain o cadenas de bloques han atraído muchísima atención en los últimos años, depositándose sobre ellas esperanzas de grandes cambios en muchas áreas de la sociedad. En este proyecto, se pretende estudiar algunos metadatos de las transacciones de la blockchain más importante, la de Bitcoin, caracterizándolos y extrayendo toda la información estadística posible. El estudio realizado para este TFG se basa en dos partes:_

_- Análisis de las transacciones con opcode OP_RETURN que agregan datos arbitrarios y permiten almacenar éstos en la cadena de bloques._

_- Estudio de la descentralización de Bitcoin a través de las curvas de Lorenz y el coeficiente de Gini._

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

```
$ git clone https://github.com/Luigini/metadatos_tfg.git
```

### Pre-requisitos 📋

_Basta con tener instalado Python 2.7_


### Instalación 🔧

_Si quieres analizar las transacciones OP_RETURN (primer apartado del estudio), debes ejecutar el archivo bloques_opreturn.py para obtener los datos en formato .json_

```
$ python bloques_opreturn.py
```


## Ejecutando las pruebas ⚙️

_Ejecuciones de programas que no necesitan sin argumentos_

```
$ python devs_commits.py 
```

```
$ python top_dirs_btc.py 
```

```
$ protocolos_categorias.py
```

```
$ protocolos_categorias_sin_unknown.py
```

```
$ tarifa_por_byte.py
```

```
$ transacciones_precio_tiempo.py
```


_Ejecuciones de programas que demandan argumentos_


```
$ python pools_hashrate.py  1d
```

```
$ python pools_hashrate.py  1m
```

```
$ python pools_hashrate.py  1y
```

```
$ python pools_hashrate.py  all
```

```
$ python exchanges_volumen.py 1d
```

```
$ python exchanges_volumen.py 1m
```

```
$ python exchanges_volumen.py 2y
```

```
$ python nodos_por.py  cliente
```

```
$ python nodos_por.py  cliente_unificados
```

```
$ python nodos_por.py  pais

```

```
$ python nodos_por.py  red
```


## Autores ✒️

* **Luis Ignacio Carballo Gómez** - *Trabajo Fin de Grado* - [Luigini](https://github.com/Luigini)
