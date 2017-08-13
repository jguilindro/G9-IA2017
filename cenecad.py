import requests
from lxml import html
from lxml import etree
import time
import sys
import json
import io
import re
from functools import reduce
utf8_parser = etree.XMLParser(encoding='utf-8')

start_urls = ["https://www.cenacad.espol.edu.ec/index.php/module/Report/action/Materias/l/0/o/{}/limit/15".format(str(x)) for x in range(0,2655,15)]
url_global = 'https://www.cenacad.espol.edu.ec'
# aulas_csv = io.open('aulas.csv', 'a')
# profesores_materia = io.open('profesores.csv', 'a', encoding='utf-8')
profesores_detalle = io.open('profesores_detalle.csv', 'a', encoding='utf-8')

materias = []
materia = {'nombre_materia': '', 'codigo_materia': '', 'creditos_teoricos': '', 'creditos_practicos': ''}
# aulas_csv.write('nombre_materia|codigo_materia|creditos_teoricos|creditos_practicos\n')
# profesores_materia.write('codigo_materia|nombre_materia|anio|semestre|profesor|paralelo|promedio\n')
#

xrange = range(1,80)
preguntas = reduce(lambda x, y: str(x) + '|'+str(y), xrange)
profesores_detalle.write('profesor|unidad|materia|paralelo|anio|periodo|estudiantes_registrados|estudiantes_evaluados|numero_estudiantes_fuera_periodo|numero_preguntas|promedio_unidad|promedio_unidad_encuesta|promedio_profesor_paralelo|promedio_estandar_paralelo|link|' + preguntas + '\n')

def hola():
    ## obtener los links de cada materia base de la pagina
    tam = len(start_urls)
    for k in range(0,tam):
        time.sleep(0.2)
        r = requests.get(start_urls[k])
        page = html.fromstring(r.text)
        # page = html.fromstring(requests.get(start_urls[k]).content)
        for i in range(2,17):
            # text = page.xpath('//*[@id="right"]/div[2]/table//tr[5]//tr[{}]//td[{}]//text()'.format(str(i), str(j)))[0]
            materia = json.dumps({})
            nombre_materia = page.xpath('//*[@id="right"]/div[2]/table//tr[5]//tr[{}]//td[{}]//text()'.format(str(i), str(2)))[0]
            codigo_materia = page.xpath('//*[@id="right"]/div[2]/table//tr[5]//tr[{}]//td[{}]//text()'.format(str(i), str(3)))[0]
            creditos_teoricos = page.xpath('//*[@id="right"]/div[2]/table//tr[5]//tr[{}]//td[{}]//text()'.format(str(i), str(4)))[0]
            creditos_practicos  = page.xpath('//*[@id="right"]/div[2]/table//tr[5]//tr[{}]//td[{}]//text()'.format(str(i), str(5)))[0]
            # obtener los cursos con nombres y codigo
            # aulas_csv.write('{},{},{},{}\n'.format(nombre_materia,codigo_materia,creditos_teoricos,creditos_practicos))
            link = page.xpath('//*[@id="right"]/div[2]/table//tr[5]//tr[{}]//td[6]//a/@href'.format(str(i)))[0]
            # print('La materia: {}'.format(link))
            parse_materia(url_global + link)

## entrar a ver historial de cada una de las materias
def parse_materia(response):
    time.sleep(0.2)
    page = html.fromstring(requests.get(response).content)
    tamano = len(page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr'))
    if (tamano != 0):
        ## primera tabla
        for i in range(2,tamano + 1):
            # guardar_profesor(i,page) ## detalles profesor primera table
            link = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]/td[8]/a/@href'.format(str(i)))[0]
            # print('El detaller profesor:  {}'.format(link))
            ## detalles por curso especifico
            parse_detalles_curso(url_global + link, link)

        ## tablas de paginacion
        tamano_pagination = len(page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[4]//tr/td/div//a'))
        print(tamano_pagination)
        for k in range(1, (tamano_pagination)):
            path_pagination = '//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[4]//tr/td/div//a[{}]/@href'.format(str(k))
            url = page.xpath(path_pagination)[0]
            # print('El detaller profesor:  {}'.format(url))
            parse_tabla(url_global + url)

# recorrer la paginacion de todo
def parse_tabla(response):
    time.sleep(0.2)
    page = html.fromstring(requests.get(response).content)
    tamano = len(page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr'))
    for i in range(2,tamano + 1):
        guardar_profesor(i,page)
        link = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]/td[8]/a/@href'.format(str(i)))[0]
        parse_detalles_curso(url_global + link, link)

def parse_detalles_curso(response, link):
    ## obtener la tabla de detaller de este progesor
    time.sleep(0.2)
    estado = True
    try:
        page = html.fromstring(requests.get(response).content)
    except:
        estado = False
        pass
    if (estado):
        guardar_paralelo(page, link)
    # sys.exit("Error message")

def guardar_profesor(i,page):
    codigo = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[1]//tr/td[3]/text()')[0]
    nombre_materia = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[1]//tr/td[3]/strong/text()')[0]
    anio = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]//td[{}]//text()'.format(str(i), str(2)))[0]
    semestre = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]//td[{}]//text()'.format(str(i), str(3)))[0]
    profesor = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]//td[{}]//text()'.format(str(i), str(4)))[0]
    paralelo = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]//td[{}]//text()'.format(str(i), str(5)))[0]
    promedio = page.xpath('//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]//td[{}]//text()'.format(str(i), str(6)))[0]
    # profesores_materia.write("{}|{}|{}|{}|{}|{}|{}\n".format(codigo.strip(),nombre_materia.strip(),anio.strip(),semestre.strip(),re.sub(' +',' ',profesor),paralelo.strip(),promedio.strip()))

def guardar_paralelo(page, link):
    profesor = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[1]/td/text()[preceding-sibling::br][3]')[0]
    profesor = profesor.split(':')[1]
    unidad =  page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[1]/text()[preceding-sibling::br][1]')[0]
    unidad = unidad.split(':')[1]
    materia = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[1]/text()[preceding-sibling::br][2]')[0]
    materia = materia.split(':')[1]
    paralelo = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[1]/text()[preceding-sibling::br][3]')[0]
    paralelo = paralelo.split(':')[1]
    anio = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[1]/text()[preceding-sibling::br][4]')[0]
    anio = anio.split(':')[1]
    periodo = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[1]/text()[preceding-sibling::br][5]')[0]
    periodo = periodo.split(':')[1]
    estudiantes_registrados = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]/text()')[0]
    estudiantes_registrados = estudiantes_registrados.split(':')[1]
    estudiantes_evaluados = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]/text()[preceding-sibling::br][1]')[0]
    estudiantes_evaluados = estudiantes_evaluados.split(':')[1]
    numero_estudiantes_fuera_periodo = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]/text()[preceding-sibling::br][2]')[0]
    numero_estudiantes_fuera_periodo = numero_estudiantes_fuera_periodo.split(':')[1]
    numero_preguntas = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]/text()[preceding-sibling::br][3]')[0]
    numero_preguntas = numero_preguntas.split(':')[1]
    promedio_unidad = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]/text()[preceding-sibling::br][4]')[0]
    promedio_unidad = promedio_unidad.split(':')[1]
    promedio_unidad_encuesta = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]/text()[preceding-sibling::br][5]')[0]
    promedio_unidad_encuesta = promedio_unidad_encuesta.split(':')[1]
    promedio_profesor_paralelo = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]//strong[1]/text()')[0].split(':')[1]
    promedio_estandar_paralelo = '-1'
    try:
        promedio_estandar_paralelo = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]//strong[2]/a/text()')[0]
    except:
        promedio_estandar_paralelo = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[1]//tr[2]/td[2]//strong[2]/text()')[0].split(':')[1]
    # 1_1, 1_2, 1_3
    tablas = page.xpath('//*[@id="right"]/div[2]/table[1]//table')
    #profesores_materia.write("{}|{}|{}|{}|{}|{}|{}\n".format(codigo.strip(),nombre_materia.strip(),anio.strip(),semestre.strip(),re.sub(' +',' ',profesor),paralelo.strip(),promedio.strip()))
    n_preguntas = 0
    preguntas_todas = []
    bandera = False
    for j in range(2, len(tablas) + 1):
        tabla = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[{}]//tr'.format(str(j)))
        # print(len(tabla))
        if (len(tabla) > 50):
                preguntas_todas = []
                break
        for i in range(3,len(tabla) + 1):
            
            try:
                numero = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[{}]//tr[{}]/td[1]/text()'.format(str(j),str(i)))[0]
                contenido = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[{}]//tr[{}]/td[2]/text()'.format(str(j),str(i)))[0]
                media = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[{}]//tr[{}]/td[3]/text()'.format(str(j),str(i)))[0]
                desviacion_estandar = '-1'
                try:
                    desviacion_estandar = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[{}]//tr[{}]/td[4]//a/text()'.format(str(j),str(i)))[0]
                except:
                    desviacion_estandar = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[{}]//tr[{}]/td[4]/text()'.format(str(j),str(i)))[0]
                puntaje_obtenido = page.xpath('//*[@id="right"]/div[2]/table[1]//tr[3]/td/table[{}]//tr[{}]/td[5]/text()'.format(str(j),str(i)))[0]
                preguntas_todas.append("{}?{}?{}?{}".format(numero.strip(),media.strip(),puntaje_obtenido.strip(),desviacion_estandar.strip()))
            except:
                print('error')
                #bandera = False
    #if (bandera == False):
        #preguntas_todas = []
        #bandera = True
    # profesores_detalle.write('profesor|unidad|materia|paralelo|anio|periodo|estudiantes_registrados|estudiantes_evaluados|numero_estudiantes_fuera_periodo|numero_preguntas|promedio_unidad|promedio_unidad_encuesta|promedio_profesor_paralelo|link|' + preguntas + '\n')
    preg = '|'.join(preguntas_todas)
    profesores_detalle.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{} \n'.format(profesor,unidad,materia,paralelo,anio,periodo,estudiantes_registrados,estudiantes_evaluados,numero_estudiantes_fuera_periodo,numero_preguntas,promedio_unidad,promedio_unidad_encuesta,promedio_profesor_paralelo,promedio_estandar_paralelo,link,preg))
    print(link)
    print(numero_preguntas)
    print(preguntas_todas)
    print('===============')

if __name__ == "__main__":
    hola()



# path = '//*[@id="right"]/div[2]/table//tr[3]/td/table//tr/td/table[2]//tr[{}]//td[{}]//text()'.format(str(i), str(j))
#             text = page.xpath(path)
