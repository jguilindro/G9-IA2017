"""
Se encargara de manejar la logica de como tratar los datos: acceso a base de datos, manejo de logica de sistema inteligente
"""
import course_selection
import json
import pandas
import models
import codecs
import csv
import numpy as np
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
	materias = []
	with codecs.open('{}.csv'.format(carrera_id), 'r','UTF-8') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			materias.append({'materia': row[0], 'nombre': row[1]})
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
		1,2,3
	]
	'estado': [1,0,0]
}

"""

def recomendacion(student_info):
	#student_info = json.loads(student_info)
	major = student_info['carrera_id']
	materias = student_info['materias']
	courses = student_info['estado']
	courses_available = course_selection.courses_available(courses,major)
	test_set = [np.squeeze(course_selection.get_feature_sample(sample).values.T.tolist(),axis=1) for (index,sample) in enumerate(materias) if courses_available[index]==1]
	difficulty = models.ANN_predict(test_set)
	student_info['materias_disponibles'] =  courses_available.tolist()
	student_info['dificultad'] = difficulty


	return student_info
