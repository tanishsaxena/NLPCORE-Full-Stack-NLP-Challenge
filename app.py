#import Libraries
import flask
from flask import Flask, render_template
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib
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
    X_person,X_place,Y_person,Y_place,labels_person,labels_place=t3.main()


    ##Visualizing based on person categpries
    plt.figure(figsize=(8,5))
    plt.scatter(X_person[:, 0], X_person[:, 1], 
    c = Y_person,
    s = 90,
    )
    plt.savefig("person.png",bbox_inches="tight")
    plt.close() 
    
    #Visualizing based on place categpries
    plt.figure(figsize=(8,5))
    plt.scatter(X_place[:, 0], X_place[:, 1], 
    c = Y_place,
    s = 90,
    )
    plt.savefig("place.png",bbox_inches="tight")
    plt.close()

    target_dir="static"

    #Changing files directory
    for file_name in os.listdir(os.getcwd()):
        if file_name=="person.png" or file_name=="place.png":
            shutil.move( file_name, os.path.join(target_dir,file_name))
  
    return render_template("task3.html",person=set(labels_person),place=set(labels_place))

#Main Condition
if __name__=="__main__":
    app.run()
