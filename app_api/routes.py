"""
Se encargara de la validacion y proceso de los request y responses
"""

from flask import jsonify,abort
import controllers

class Carreras:
	## obtener todas las carreras
	def get_all():
		# if len(task) == 0:
  #       	abort(404)
		return jsonify({'datos': controllers.obtenerCarreras()})

	## obtener todas las materias de una carrra
	def get_by_carrera(carrera_id):
		return jsonify({'datos': controllers.obtenerMateriasCarrera(carrera_id)})


class Materias:
	def get_all():
		return 'todas materias'

	
class Recomendacion:
	def recomendar(entradas):
		return jsonify({'datos': controllers.recomendacion(entradas)})