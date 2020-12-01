#import Libraries
import nltk
import operator
import json


#Word Frequemcy generator
def word_count(str):
    words = str.split()
    counts=dict(nltk.FreqDist(words))
    final=[]
    for word in range(len(list(counts.keys()))):
        temp={"text":"","value":None}
        temp["text"]=list(counts.keys())[word]
        temp["value"]=list(counts.values())[word]
        final.append(temp)    
    sorted_count= sorted(counts.items(), key=operator.itemgetter(1),reverse=True)
    return final,sorted_count[:6]

#Main Function
def main():

    #Json opening
    file=open("Database\\task2.json",)
    data = json.load(file) 
    data = json.loads(data) 
    
    #Getting all cluster points
    clusters=[]
    for doc in range(len(data)):
        clusters.append(data[doc]["clusters"])

    #Processing data for visualization
    num_clusters=list(set(clusters))
    resultant=[]
    for clust in num_clusters:
        javascript={"Cluster":"","Data":[]}
        document=[]
        for doc in data:
            if doc["clusters"]==clust:
                document.append(doc)
        text=""
        for dat in document:
            text+=dat["content"]
            text+=" "
        text=text.lower()
        resultant_data,tag=word_count(text)
        javascript["Data"]=resultant_data
        cluster=""
        for index in range(len(tag)-3):
            cluster+=tag[index][0][:3-index]
        javascript["Cluster"]="Cluster "+cluster+" With Top 3 Most Frequent Words "+tag[0][0]+" "+tag[1][0]+" "+tag[2][0]
        resultant.append(javascript)
    return resultant