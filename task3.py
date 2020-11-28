#Import Libraries
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import io
import base64
import json
import threading
import queue

def process_person(q,person_doc):
    person={"Title":[],"Doc_Number":[],"Cluster":[]}

    for perdoc in person_doc:
        person["Cluster"].append(perdoc["cluster"])
        person["Doc_Number"].append(perdoc["docNumber"])
        person["Title"].append(perdoc["title"])

    #Process to label titles
    df_person_categorization=pd.DataFrame.from_dict(person)

    person_titles=df_person_categorization["Title"].to_list()

    le = preprocessing.LabelEncoder()

    le_person_titles=le.fit_transform(person_titles)

    df_person_categorization["labeled_titled"]=le_person_titles

    #PCA Analyses
    X_person=np.array(df_person_categorization[["Doc_Number","labeled_titled"]])
    pca = PCA(n_components=2)
    principalComponents_person = pca.fit_transform(X_person)

    #Final Datafreame Creation
    final_person=pd.DataFrame(principalComponents_person,columns=["Doc_Number","labeled_title"])
    final_person["Persons"]=df_person_categorization["Cluster"]
    final_person["Titles"]=df_person_categorization["Title"]

    cols=final_person.columns.to_list()
    cols = cols[-1:] + cols[:-1]
    final_person=final_person[cols]

    q.put(final_person)




def process_place(p,place_doc):
    place={"Title":[],"Doc_Number":[],"Cluster":[]}

    for pladoc in place_doc:
        place["Cluster"].append(pladoc["cluster"])
        place["Doc_Number"].append(pladoc["docNumber"])
        place["Title"].append(pladoc["title"])

    #Process to label titles
    df_place_categorization=pd.DataFrame.from_dict(place)

    place_titles=df_place_categorization["Title"].to_list()

    le = preprocessing.LabelEncoder()

    le_place_titles=le.fit_transform(place_titles)

    df_place_categorization["labeled_titled"]=le_place_titles

    #PCA Analyses
    X_place=np.array(df_place_categorization[["Doc_Number","labeled_titled"]])
    pca = PCA(n_components=2)
    principalComponents_place = pca.fit_transform(X_place)

    #Final Datafreame Creation
    final_place=pd.DataFrame(principalComponents_place,columns=["Doc_Number","labeled_title"])
    final_place["Places"]=df_place_categorization["Cluster"]
    final_place["Titles"]=df_place_categorization["Title"]

    cols=final_place.columns.to_list()
    cols = cols[-1:] + cols[:-1]
    final_place=final_place[cols]

    p.put(final_place)


#Main Function
def main():

    file=open("Database\\task3Person.json",)
    data_person = json.load(file) 
    data_person = json.loads(data_person) 

    file=open("Database\\task3Place.json",)
    data_place = json.load(file) 
    data_place = json.loads(data_place) 

    person=queue.Queue()
    place=queue.Queue()

    th_person=threading.Thread(target=process_person,args=(person,data_person,))
    th_place=threading.Thread(target=process_place,args=(place,data_place,))

    th_person.start()
    th_place.start()

    th_person.join()
    th_place.join()

    return person.get(),place.get()
