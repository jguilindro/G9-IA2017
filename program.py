import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# horas = input('Ingrese la cantidad de horas disponibles a la semana: ')
# print('Cantidad de horas disponibles: ', horas)

# create data frame from csv and filter by 'fiec'
profe = pd.read_csv('profesores.csv', delimiter='|')
profe_fiec = profe[profe.codigo_materia.str.contains('FIEC')]

# labels, unique = pd.factorize(data.nombre_materia) TODO

profe_fiec_2016_2S = profe_fiec[
                                (profe_fiec.anio == 2016) &
                                (profe_fiec.semestre== '2S')
                                ]

data = profe_fiec_2016_2S.groupby(
                                ['profesor','nombre_materia'],
                                as_index=False
                                ).mean()

def f_easy(x):
    return (1/(1+np.exp(0.75*(-x+86))))

def f_moderate(x):
    return 1 - np.tanh(0.15*(x-80))**2

def f_hard(x):
    return (1/(1+np.exp(0.75*(x-74))))

teacher_rating = data.promedio.sort_values()

difficulty_easy = f_easy(teacher_rating)
difficulty_moderate = f_moderate(teacher_rating)
difficulty_hard = f_hard(teacher_rating)

plt.title('Course Difficulty')
plt.xlabel('Teacher Review Score')
plt.plot(teacher_rating, difficulty_easy)
plt.plot(teacher_rating, difficulty_moderate)
plt.plot(teacher_rating, difficulty_hard)
plt.show()


Demo:
    Programación orientada a objetos
    Sistemas de bases de datos
    Fundamentos del diseno digital
    Metodologia de la investigacion
    Ciencias de la computacion aplicada a la resolucion de problemas
