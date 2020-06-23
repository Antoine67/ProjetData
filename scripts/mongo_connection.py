#Import pymongo to connect to database
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

#Localhost
client = MongoClient('localhost', 27017)

#Get database and vehicules collection
db = client["DataProject"]
stats = db["stats"]

def insert_stats(x,y, name, x_label="", y_label="", specification="", dataset_name=""):
    dict_stats_points = {
        'name':name,
        'x':x,
        'y':y,
        "x_label":x_label,
        "y_label":y_label,
        "specification":specification,
        "dataset_name":dataset_name,
        
    }
    
    stats.insert_one(dict_stats_points)



def insert_multiple_stats(x_array, y_array, name, x_label, y_label, specification_array, dataset_name_array):
    
    if(len(x_array) != len(y_array)):
        raise Exception('Len X != Len Y !')
    
    length = len(x_array);
    for i in range(length):
        insert_stats(x_array[i], y_array[i], name, x_label, y_label, specification_array[i],dataset_name_array[i] )




def get_stats(name):
    return stats.find({ "name": name});


def show_stats(name):
    stat = get_stats(name)[0]
    x = stat['x']
    y = stat['y']
    
    fig = plt.figure()
    fig.suptitle(stat['name'], fontsize=14, fontweight='bold')
    
    ax = fig.add_subplot(111)
    ax.set_xlabel(stat['x_label'])
    ax.set_ylabel(stat['y_label'])
    plt.plot(x, y)
    plt.show()

"""
if __name__ == '__main__':
    insert_stats([1,2,3,4,5],[4,8,7,54,4], 'test','s','exec')
    
    insert_multiple_stats([[1,2,3],[1,2,3]], [[10,15,25],[3,6,9]],"temps en fct nb solutions", "nb solutions","temps", ['tabu','simulated'],['n32-k5','n32-k5'])
    print(get_stats('test')[0])
    show_stats("test")
"""