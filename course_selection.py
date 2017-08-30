import numpy as np

def courses_available(courses, major):
    # Major = {CC,EE,TC,TM}
    mayor_dep = np.genfromtxt('./tmp/cc_course_dependencies/{}.csv'.format(major), delimiter=',',filling_values=0)
    mayor_dep = mayor_dep[1:,1:]
    mayor_dep_ = np.sum(mayor_dep,axis=1)
    mayor_dep_val = np.matmul(mayor_dep,courses) == mayor_dep_
    always_available = 1-np.amax(mayor_dep,axis=1)
    return np.heaviside(np.multiply(mayor_dep_val+always_available,1-np.asarray(courses)),0)
