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



def insert_multiple_stats(x_array, y_array, name, x_label, y_label, specification_array, dataset_name):
    
    if len(x_array) != len(y_array):
        raise Exception('Len X != Len Y !')
    
    length = len(x_array);
    for i in range(length):
        insert_stats(x_array[i], y_array[i], name, x_label, y_label, specification_array[i],dataset_name )




def get_first_stat(name):
    return stats.find({ "name": name});


def get_avg_stats(name, specification, dataset_name):
    #return stats.find({ "name": name});
    return stats.aggregate([{
        '$match': {
            'name': name, 
            'specification': specification,
            'dataset_name':dataset_name,
        }
    }, 
        
        {
        "$unwind": {
            "path": "$y",
            "includeArrayIndex": "rowY"
        }
    },
        {
        "$unwind": {
            "path": "$x",
            "includeArrayIndex": "rowX"
        }
    },
    {
        "$group": {
            "_id": {
                "name": "$name",
                "rowY": "$rowY",
               
            },
            "mean_y": {
                "$avg": "$y"
            }
        }
    },
    
    {
        "$group": {
            "_id": "$_id.name",
            "mean_y": {
                "$push": "$mean_y"
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "name": "$_id",
            "mean_y": 1
        }
    }
])

'''
    {
        "$sort": {
            "_id.name": 1,
            "_id.rowY": 1
        }
    },
    '''


def get_avg_stats2(name, specification, dataset_name):
    data = stats.find({'name':name,'specification':specification,'dataset_name':dataset_name})
    first_occ = data[0]
    # GROUP BY X
    points = {}
    for d in data:
        for i in range(len(d['x'])):
            x = d['x'] 
            y = d['y']
            if x[i] in points:
                points[x[i]].append(y[i])
            else :
                 points[x[i]] = [y[i]]
   
    
    
    #Moyenne
    final_points = {}
    for key, value in points.items():
        moy = 0
        final_points[key] = np.average(np.array(value))
    final_dic = {'x':list(final_points.keys()),
                 'y':list(final_points.values()),
                 'x_label':first_occ['x_label'],
                 'y_label':first_occ['y_label'],
                 'specification':specification,
                 'dataset_name':dataset_name,
                 'name':name
                }        
    return final_dic         
        
"""
if __name__ == '__main__':

    #insert_multiple_stats([[1,2,3],[1,2,3]], [[1,2,3],[3,6,9]],"temps en fct nb solutions", "nb solutions","temps", ['tabu','simulated'],'n32-k5'])
    a = get_avg_stats2("temps en fct nb solutions", "tabu","n32-k5")
    print(a)

"""