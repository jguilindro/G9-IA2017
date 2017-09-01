import numpy as np
import pandas as pd
import models

def courses_available(courses, major):
    # Major = {CC,EE,TC,TM}
    mayor_dep = np.genfromtxt('./tmp/cc_course_dependencies/{}_.csv'.format(major), delimiter=',',filling_values=0)
    mayor_dep = mayor_dep[1:,1:]
    mayor_dep_ = np.sum(mayor_dep,axis=1)
    mayor_dep_val = np.matmul(mayor_dep,courses) == mayor_dep_
    always_available = 1-np.amax(mayor_dep,axis=1)
    return np.heaviside(np.multiply(mayor_dep_val+always_available,1-np.asarray(courses)),0)

def get_feature_sample(course):
    df = pd.read_csv('./tmp/features.csv',sep='|')
    sample = df.groupby(['codigo_materia']).mean().reset_index()
    col_select = sample.columns[7:-1]
    return sample[col_select].loc[sample['codigo_materia']==course]

def train_ann(epochs=100):
    mayor_dep = np.genfromtxt('./tmp/features_training.csv', delimiter='|',filling_values=0)
    training_input = mayor_dep[:,11:-1]
    training_target = mayor_dep[:,-1].astype(int)
    models.ANN_train(training_input, training_target,epochs=epochs)
