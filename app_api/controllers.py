"""
Se encargara de manejar la logica de como tratar los datos: acceso a base de datos, manejo de logica de sistema inteligente
"""

import json

"""
EJEMPLO

GET 

Response
carreras = [
	    {
	        'id': 1,
	        'nombre': 'Computacion',
	    },
	    {
	        'id': 1,
	        'nombre': 'Electronica',
	    },
	]

"""
def obtenerCarreras():
	carreras = [
	    {
	        'id': 1,
	        'nombre': 'Computacion',
	    },
	    {
	        'id': 1,
	        'nombre': 'Electronica',
	    },
	]
	return carreras


"""
GET carrera_id

## Request


## Response
materias = [
		{
			'id': 1,
			'nombre': 'Analisis Algoritmos',
			'codigo': 'FIEC55',
		},
		{
			'id': 2,
			'nombre': 'Programacion Orientada a objecto',
			'codigo': 'FIEC55',
		},
		{
			'id': 3,
			'nombre': 'Inteligencia Artificial',
			'codigo': 'FIEC55',
		},
	]

"""
def obtenerMateriasCarrera(carrera_id):
	## buscar en la base de datos o cualquier cosa el por carrera_id
	materias = [
		{
			'id': 1,
			'nombre': 'Analisis Algoritmos',
			'codigo': 'FIEC55',
		},
		{
			'id': 2,
			'nombre': 'Programacion Orientada a objecto',
			'codigo': 'FIEC55',
		},
		{
			'id': 3,
			'nombre': 'Inteligencia Artificial',
			'codigo': 'FIEC55',
		},
	]
	return materias


"""

POST

## Request 
{
	"carrera_id": 1,
	"carreras": [
		1,
		5,
		10,
		50
	],
	"horas": 50
}

## Response (aqui no se bien que info se enviara)
{
	"materias": [
		{
			"id": 1,
			"nombre": "Algoritmos",
			"curso": "",

		}
	]
}

"""

def recomendacion(entradas):
	carrera_id = entradas['carrera_id']
	carreras = entradas['carreras']
	horas = entradas['horas']
	resp = [
		{
			"id": 1,
			"nombre": "Algoritmos",
			"curso": "",

		}
	]

	return resp