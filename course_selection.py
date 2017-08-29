import numpy as np

def courses_available(courses, major):
    # Major = {CC,EE,TC,TM}
    mayor_dep = np.genfromtxt('./tmp/cc_course_dependencies/{}.csv'.format(major), delimiter=',',filling_values=0)
    mayor_dep = mayor_dep[1:,1:]
    always_available = 1-np.amax(mayor_dep,0)
    return np.multiply(np.matmul(mayor_dep,courses)+always_available,1-np.asarray(courses))
