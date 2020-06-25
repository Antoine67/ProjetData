from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

import statsmodels.api as sm
import statsmodels.stats.api as sms
from statsmodels.iolib.smpickle import load_pickle
from scipy import stats
import pylab as py
from tqdm import tqdm


# Connexion
client = MongoClient('localhost', 27017)
db = client['DataProject']
collection_trafic_stamped = db['vehicules_stamped']
collection_stats_vehicules_model = db['collection_stats_vehicules_model']

def get_prediction(num_arete, hour, minute = 0):
    m, s = False, False
    if(hour <= 9  or hour >7):
        m = True
        hour = hour - 7
    elif(hour <= 19 or hour >17):
        s  = True
        hour = hour -17
    creneau = 0 if m else 1
    res = load_pickle("../data/Regression/vehicules_aretes_"+ str(creneau) + "_n" + str(num_arete)+".pickle")
   

    #print(res.summary())
    pred = res.predict(exog=[hour, minute])

    y_pred = res.params[0]+res.params[1]*(hour*60 + minute)

    return y_pred


def create_and_store_stats_model():
    
    vehicules_par_arete_matin = list(db.vehicules_stamped.aggregate([
        {"$project":{"num_arete":1, "heures":{"$hour":"$datetime"}, "nb_vehicules":1}},
        {"$match":{"heures":{"$lte":9, "$gte":7}}},
        {"$group":{"_id":"$num_arete", 
                   "nb_vehicules":{"$avg":"$nb_vehicules"}}},
        {"$sort":{"nb_vehicules":-1}}
    ]))
    
    vehicules_par_arete_soir = list(db.vehicules_stamped.aggregate([
        {"$project":{"num_arete":1, "heures":{"$hour":"$datetime"}, "nb_vehicules":1}},
        {"$match":{"heures":{"$lte":19, "$gte":17}}},
        {"$group":{"_id":"$num_arete", 
                   "nb_vehicules":{"$avg":"$nb_vehicules"}}},
        {"$sort":{"nb_vehicules":-1}}
    ]))
    
    
    w = 500;
    
    pred = {'0': list([None] * w) , '1': list([None] * w)}
    
    
    for i,vehicules_par_arete in enumerate([vehicules_par_arete_matin,vehicules_par_arete_soir]):
        for j in tqdm(range(len(vehicules_par_arete)), desc="Vehicule sur le créneau horaire n°"+str(i)):
            arete = vehicules_par_arete[j]["_id"]
            
            if(i == 0):
                vehicules_arete = db.vehicules_stamped.aggregate([
                    {"$match":{"num_arete":{"$eq":arete}}},
                    {"$project":{"temps":{"heures":{"$hour":"$datetime"}, 
                                          "minutes":{"$minute":"$datetime"}},
                                "nb_vehicules":1}},
                    {"$match":{"temps.heures":{"$lte":9, "$gte":7}}},
                     {"$sort":{"temps":1}}])
                
                xs = pd.date_range("2020-01-01 07:01", "2020-01-01 09:00", freq = "min").to_pydatetime().tolist()
            else:
                vehicules_arete = db.vehicules_stamped.aggregate([
                    {"$match":{"num_arete":{"$eq":arete}}},
                    {"$project":{"temps":{"heures":{"$hour":"$datetime"}, 
                                          "minutes":{"$minute":"$datetime"}},
                                "nb_vehicules":1}},
                    {"$match":{"temps.heures":{"$lte":19, "$gte":17}}},
                     {"$sort":{"temps":1}}])
                
                xs = pd.date_range("2020-01-01 17:01", "2020-01-01 19:00", freq = "min").to_pydatetime().tolist()
            xs = [e for sub in zip(xs, xs, xs, xs, xs) for e in sub] 
            trafics = [trafic["nb_vehicules"] for trafic in vehicules_arete]
            ys = trafics[:600]
        
            if(i == 0):
                X = [(date.hour-7)*60+date.minute for date in xs]
            else:
                X = [(date.hour-17)*60+date.minute for date in xs]
            X = np.append(arr = np.ones((len(X), 1)).astype(int), values = np.array([X]).T, axis = 1)
            
            #
            regressor_OLS = sm.OLS(endog = ys, exog = X).fit()
            y_pred = regressor_OLS.params[0]+regressor_OLS.params[1]*X[:,1]
            
            pred[str(i)][j] = y_pred.tolist()
            
            regressor_OLS.save("../data/Regression/vehicules_aretes_"+ str(i) + "_n" + str(j)+".pickle")
            #Résidus
            """
            fig, ax = plt.subplots()
            ax.scatter(X[:,1], regressor_OLS.resid, alpha=0.3)
            ax.set(title="Résidus de la régression linéairepour l'arête n°"+str(i), xlabel="Temps", ylabel="Residus")
            plt.show()
            """
            
            #Régression linéaire
            """
            fig, ax = plt.subplots()
            ax.scatter(X[:,1], ys, alpha=0.3)
            ax.set(title="Régression linéaire pour l'arête n°"+str(i), xlabel="Temps", ylabel="Trafic")
            ax.plot(X[:,1], y_pred, linewidth=3)
            plt.show()
            """
            
    #collection_stats_vehicules_model.drop()
    #collection_stats_vehicules_model.insert_one(pred)
    
    #print(pred)
#create_and_store_stats_model()
print(get_prediction(0,7,20))