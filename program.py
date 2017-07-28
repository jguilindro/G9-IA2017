import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# horas = input('Ingrese la cantidad de horas disponibles a la semana: ')
# print('Cantidad de horas disponibles: ', horas)

# Load expert table
expert = pd.read_csv('expert_table.csv')

def hour_input(hour):
    if hour <= 9:
        hour = 5
    elif hour < 40:
        hour -= hour % 10
    else:
        hour = 40
    return hour

def get_courses_distro(hour):
    hour = hour_input(hour)
    return expert[expert['hoursAvailable'] == hour]

# create data frame from csv and filter by 'fiec', year amd semestre '2S'
profe = pd.read_csv('profesores.csv', delimiter='|')
profe_fiec = profe[profe.codigo_materia.str.contains('FIEC')]
profe_fiec_2016_2S = profe_fiec[
                                (profe_fiec.anio == 2016) &
                                (profe_fiec.semestre== '2S')
                                ]

# labels, unique = pd.factorize(data.nombre_materia) TODO

data_mean = profe_fiec_2016_2S.groupby(
                                ['nombre_materia'],
                                as_index=False
                                ).mean()
del data_mean['anio']
data_std = profe_fiec_2016_2S.groupby(
                                ['nombre_materia'],
                                ).std()
data_mean['std'] = data_std['promedio']
data_mean = data_mean.fillna(value=0)

sorted_data = data_mean.sort_values('promedio')

# Membership Functions
def f_easy(x):
    return (1/(1+np.exp(0.75*(-x+86))))

def f_moderate(x):
    return 1 - np.tanh(0.15*(x-80))**2

def f_hard(x):
    return (1/(1+np.exp(0.75*(x-74))))


teacher_rating = sorted_data.promedio

difficulty_easy = f_easy(teacher_rating)
difficulty_moderate = f_moderate(teacher_rating)
difficulty_hard = f_hard(teacher_rating)

sorted_data['easy'] = difficulty_easy
sorted_data['moderate'] = difficulty_moderate
sorted_data['hard'] = difficulty_hard

def print_title(title):
    print "{}{}{}{}{}".format('\n',title,'\n','='*len(title),'\n')

def get_recommended_courses(hours, n=5):
    course_distro = get_courses_distro(hours)
    _, easy, moderate, hard = course_distro.values[0]
    easy_title, moderate_title, hard_title = 'EASY COURSES', 'MODERATE COURSES', 'HARD COURSES'
    if easy:
        print_title(easy_title)
        print('\n'.join((sorted_data.sort_values('easy', ascending=False))[1:n * easy + 1]['nombre_materia'].values))

    if moderate:
        print_title(moderate_title)
        print('\n'.join((sorted_data.sort_values('moderate', ascending=False))[1:n * moderate + 1]['nombre_materia'].values))

    if hard:
        print_title(hard_title)
        print('\n'.join((sorted_data.sort_values('hard', ascending=False))[1:n *hard + 1]['nombre_materia'].values))

plt.title('Course Difficulty')
plt.xlabel('Teacher Review Score')
plt.plot(teacher_rating, difficulty_easy)
plt.plot(teacher_rating, difficulty_moderate)
plt.plot(teacher_rating, difficulty_hard)
plt.show()
