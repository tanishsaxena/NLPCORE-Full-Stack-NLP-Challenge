#Import Libraries
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import io
import base64
import json

#Data Processing
def dataProcess(person_doc,place_doc):

    #Dictionary to store data fetched from db
    person={"Cluster":[],"Doc_Number":[],"Title":[]}
    place={"Cluster":[],"Doc_Number":[],"Title":[]}

    #Fetching Collection from db
    for perdoc in person_doc:
        person["Cluster"].append(perdoc["cluster"])
        person["Doc_Number"].append(perdoc["docNumber"])
        person["Title"].append(perdoc["title"])
        
    for pladoc in place_doc:
        place["Cluster"].append(pladoc["cluster"])
        place["Doc_Number"].append(pladoc["docNumber"])
        place["Title"].append(pladoc["title"])

    #Dataframe conversion and processing of data
    df_person_categorization=pd.DataFrame.from_dict(person)
    df_place_categorization=pd.DataFrame.from_dict(place)

    person_labels=df_person_categorization["Cluster"].to_list()
    place_labels=df_place_categorization["Cluster"].tolist()

    person_titles=df_person_categorization["Title"].to_list()
    place_titles=df_place_categorization["Title"].tolist()

    ##Label Encoding to neutralize the data
    le = preprocessing.LabelEncoder()

    le_person_labels=le.fit_transform(person_labels)
    le_place_labels=le.fit_transform(place_labels)

    le_person_titles=le.fit_transform(person_titles)
    le_place_titles=le.fit_transform(place_titles)


    df_person_categorization["Title"]=le_person_titles
    df_place_categorization["Title"]=le_place_titles

    df_person_categorization["Cluster"]=le_person_labels
    df_place_categorization["Cluster"]=le_place_labels

    # X data for principle component analyses
    X_person=np.array(df_person_categorization[["Doc_Number","Title"]])
    X_place=np.array(df_place_categorization[["Doc_Number","Title"]])

    #Principle Component Analysis
    pca = PCA(n_components=2)
    principalComponents_person = pca.fit_transform(X_person)
    principalComponents_place = pca.fit_transform(X_place)

    # Y Values for person and place clusters
    y_person=list(df_person_categorization["Cluster"])
    y_place=list(df_place_categorization["Cluster"])

    #returning pca components and cluster values for both person and place categories
    return principalComponents_person,principalComponents_place,y_person,y_place,person_labels,place_labels

#Main Function
def main():

    file=open("Database\\task3Person.json",)
    data_person = json.load(file) 
    data_person = json.loads(data_person) 

    file=open("Database\\task3Place.json",)
    data_place = json.load(file) 
    data_place = json.loads(data_place) 

    X_person,X_place,Y_person,Y_place,labels_person,labels_place=dataProcess(data_person,data_place)

    return X_person,X_place,Y_person,Y_place,labels_person,labels_place
    
