#import Libraries
import flask
from flask import Flask, render_template
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib
import re
matplotlib.use('Agg')
import json
from flask_cors import CORS

#Flask App Generation
app = flask.Flask(__name__,static_folder="static\\")
app.config["DEBUG"] = True
CORS(app)
#Routing Functions
@app.route("/")
def index():
    return render_template("Main.html")


@app.route('/task1', methods=['GET','POST'])
def task1():
    import task1 as t1
    obj=t1.task1("Data")
    result=obj.main()
    occ=[]
    occ.append(["Word","Occurence"])
    freq=[]
    freq.append(["Word","Frequency"])
    for i in range(100):
        tempoccu=[]
        tempoccu.append(str(result["Attribute"].iloc[i]))
        tempoccu.append(int(result["Occur"].iloc[i]))
        occ.append(tempoccu)

        tempfreq=[]
        tempfreq.append(str(result["Attribute"].iloc[i]))
        tempfreq.append(int(result["Freq"].iloc[i]))
        freq.append(tempfreq)

    data={"Occur":occ,"Freq":freq}
    return json.dumps(data,indent=4)

@app.route('/task2', methods=['GET','POST'])
def task2():
    import task2 as t2
    resultant=t2.main()
    return json.dumps(resultant)

@app.route('/task3', methods=['GET','POST'])
def task3():
    import task3 as t3
    df_person,df_place=t3.main()


    person_title_temp=[re.sub('[^a-zA-Z0-9 \n\.]', '', a) for a in df_person["Titles"]]
    df_person["Titles"]=person_title_temp
    df_person["bubble_size"]=[0.3 for i in range(len(df_person))]

    place_title_temp=[re.sub('[^a-zA-Z0-9 \n\.]', '', a) for a in df_place["Titles"]]
    df_place["Titles"]=place_title_temp
    df_place["bubble_size"]=[0.1 for i in range(len(df_place))]

    person_cols=list(df_person.columns)
    place_cols=list(df_place.columns)

    resultant_person=df_person.values.tolist()
    resultant_person.append(person_cols)
    resultant_person=resultant_person[-1:]+resultant_person[:-1]

    resultant_place=df_place.values.tolist()
    resultant_place.append(place_cols)
    resultant_place=resultant_place[-1:]+resultant_place[:-1]

    data={"person":resultant_person,"place":resultant_place}
    return json.dumps(data)
#Main Condition
if __name__=="__main__":
    app.run()
