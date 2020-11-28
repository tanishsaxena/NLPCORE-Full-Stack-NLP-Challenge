#import Libraries
import flask
from flask import Flask, render_template
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib
import re
matplotlib.use('Agg')

#Flask App Generation
app = flask.Flask(__name__,static_folder="static\\")
app.config["DEBUG"] = True

#Routing Functions
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/task1', methods=['GET','POST'])
def task1():
    import task1 as t1
    obj=t1.task1("Data")
    result=obj.main()
    return render_template('task1.html',hist1Att=result["Attribute"][:100],hist1Val=result["Occur"][:100],hist2Att=result["Attribute"][:100],hist2Val=result["Freq"][:100])


@app.route('/task2', methods=['GET','POST'])
def task2():
    import task2 as t2
    resultant=t2.main()
    return render_template('task2.html',data=resultant)

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

    return render_template("task3.html",person=resultant_person,place=resultant_place)

#Main Condition
if __name__=="__main__":
    app.run()
