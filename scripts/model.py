from pymongo import MongoClient
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

import statsmodels.api as sm
import statsmodels.stats.api as sms
from scipy import stats
import pylab as py


# Connexion

client = MongoClient('localhost', 27017)
db = client['DataProject']
collection_trafic_stamped = db['vehicules_stamped']


# Requete vehicule/minute
vehicules_par_minutes = list(collection_trafic_stamped.aggregate([
    {"$project":{"temps":{"heures":{"$hour":"$datetime"}, 
                          "minutes":{"$minute":"$datetime"}},
                 "num_arete":1,
                 "nb_vehicules":1}},
    {"$group":{"_id":{"heures":"$temps.heures", "minutes":"$temps.minutes"}, 
               "nb_vehicules":{"$avg":"$nb_vehicules"}}},
    {"$sort":{"_id":1}}
]))
trafics = [trafic["nb_vehicules"] for trafic in vehicules_par_minutes]





vehicules_par_arete = list(db.vehicules_stamped.aggregate([
    {"$project":{"num_arete":1, "heures":{"$hour":"$datetime"}, "nb_vehicules":1}},
    {"$match":{"heures":{"$lte":9, "$gte":7}}},
    {"$group":{"_id":"$num_arete", 
               "nb_vehicules":{"$avg":"$nb_vehicules"}}},
    {"$sort":{"nb_vehicules":-1}}
]))

for arete in db.vehicules_stamped.find().limit(5):
    #arete_max, arete_min = vehicules_par_arete[0]["_id"], vehicules_par_arete[-1]["_id"]
    
    print(arete)
    vehicules_arete_max = db.vehicules_stamped.aggregate([
        {"$match":{"num_arete":{"$eq":arete["_id"]}}},
        {"$project":{"temps":{"heures":{"$hour":"$datetime"}, 
                              "minutes":{"$minute":"$datetime"}},
                    "nb_vehicules":1}},
        {"$match":{"temps.heures":{"$lte":9, "$gte":7}}},
         {"$sort":{"temps":1}}])
    
    
    
    xs = pd.date_range("2020-01-01 07:01", "2020-01-01 09:00", freq = "min").to_pydatetime().tolist()
    xs = [e for sub in zip(xs, xs, xs, xs, xs) for e in sub] 
    trafics = [trafic["nb_vehicules"] for trafic in vehicules_arete_max]
    ys = trafics[:600]
    
    
    
    X = [(date.hour-7)*60+date.minute for date in xs]
    X = np.append(arr = np.ones((len(X), 1)).astype(int), values = np.array([X]).T, axis = 1)
    regressor_OLS = sm.OLS(endog = ys, exog = X).fit()
    y_pred = regressor_OLS.params[0]+regressor_OLS.params[1]*X[:,1]
    
    fig, ax = plt.subplots()
    ax.scatter(X[:,1], regressor_OLS.resid, alpha=0.3)
    ax.set(title="Résidus de la régression linéaire.", xlabel="Temps", ylabel="Residus")
    #plt.show()
    
    #
    fig, ax = plt.subplots()
    ax.scatter(X[:,1], ys, alpha=0.3)
    ax.set(title="Régression linéaire l'arete la moins congéstionnée.", xlabel="Temps", ylabel="Trafic")
    ax.plot(X[:,1], y_pred, linewidth=3)
plt.show()
