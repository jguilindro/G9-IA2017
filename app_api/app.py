"""
Aqui se definiran las rutas del api y del cliente
"""

import json
from flask import Flask
from flask import request, send_from_directory,make_response,jsonify,request
import os
from routes import Carreras
from routes import Recomendacion


root_dir = os.path.dirname(os.getcwd())
app = Flask(__name__,static_folder=os.path.join(root_dir, 'app_client'),static_url_path='')

"""
API rutas
"""

## devuelve el json definido

# EJEMPLO GET http://localhost:5000/api/carreras
@app.route('/api/carreras')
def carreras_api():
    return Carreras.get_all()

## enviar el id de la carrera y devuelve el json definido en controllers
# EJEMPLO GET http://localhost:5000/api/carreras/1
@app.route('/api/carreras/<int:carrera_id>',methods=['GET'])
def carrera_materia_api(carrera_id):
    return Recomendacion.get_by_carrera(carrera_id)

## en el cuerpo del requerimiento recibe un array de materias cursadas(solo los id), las horas que puede tomar, la carrera. Ver ejemplo en controlador
# EJEMPLO POST http://localhost:5000/api/recomendacion  (no olvidar el cuerpo del json)
@app.route('/api/recomendacion',methods=['POST'])
def recomendacion_api():
	req = request.get_json(force=True, silent=True)
	return Recomendacion.recomendar(req)

"""
OJO
falta todavia el api de recomendacion, tenemos que definir como sera

"""

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



"""
Vistas en Clientes, instalar las dependencias con npm install
"""
@app.route('/', methods=['GET'])
def index():
	return send_from_directory(os.path.join(root_dir, 'app_client'), 'index.html')

@app.route('/experts', methods=['GET'])
def experts_client():
	return send_from_directory(os.path.join(root_dir, 'app_client','experts'), 'experts.html')

@app.route('/novices', methods=['GET'])
def novices_client():
	return send_from_directory(os.path.join(root_dir, 'app_client','novices'), 'novices.html')

if __name__ == '__main__':
    app.run(debug=True)
