#Import pymongo to connect to database
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

#Localhost
client = MongoClient('localhost', 27017)

#Get database and vehicules collection
db = client["DataProject"]
stats = db["stats"]


def insert_stats(x,y, name, x_label="", y_label=""):
    dict_stats_points = {
        'name':name,
        'x':x,
        'y':y,
        "x_label":x_label,
        "y_label":y_label,
        
    }
    
    stats.insert_one(dict_stats_points)


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

'''
if __name__ == '__main__':
    insert_stats([1,2,3,4,5],[4,8,7,54,4], 'test','s','exec')
    print(get_stats('test')[0])
    show_stats("test")
'''