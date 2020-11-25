import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import os
import json
import pandas as pd
import re
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import nltk
from nltk.corpus import stopwords 
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm


class task3:
    
    def __init__(self,link):
        self.df=task3.data(link)

    def main(self):
        content,titles=task3.content_title(self.df)
        Total_Persons,Total_Places,person_place_category=task3.spacyAlgo(content,titles)
        Distinct_total_persons=set(Total_Persons)
        Distinct_total_places=set(Total_Places)
        df_person_format,df_place_format=task3.freqDist(person_place_category,Distinct_total_persons,Distinct_total_places)
        person_categorization,place_categorization=task3.categorization(person_place_category,df_person_format,df_place_format)
        
        person_resultant=[]
        place_resultant=[]
        
        for doc in range(len(person_categorization["Cluster"])):
            person_resultant.append({"cluster":person_categorization["Cluster"][doc],"docNumber":person_categorization["Doc_Number"][doc],"title":person_categorization["Title"][doc]})
        for doc in range(len(place_categorization["Cluster"])):
            place_resultant.append({"cluster":place_categorization["Cluster"][doc],"docNumber":place_categorization["Doc_Number"][doc],"title":place_categorization["Title"][doc]})

        #Storing data in Database as json
        person_resultant=json.dumps(person_resultant)
        place_resultant=json.dumps(place_resultant)
        with open('task3Person.json', 'w') as f:
            json.dump(person_resultant, f)
        with open('task3Place.json', 'w') as g:
            json.dump(place_resultant, g)


    @classmethod
    def data(cls,link):
        df_rows = []
        folder = os.fsencode(link)
        for file in os.listdir(folder):
            filename = os.fsdecode(file)
            if filename.endswith('.json'):
                filename = os.fsdecode(folder)+"\\"+filename
                with open(os.fsdecode(filename), mode='r') as json_file:
                    data = json.load(json_file)
                    df_rows.append(data)
        newDF = pd.DataFrame(df_rows)
        return newDF

    @classmethod
    def content_title(cls,newDF):
        content=[]
        titles=[]
        for doc in range(len(newDF)):
            text=""
            for section in newDF["sections"][doc]:
                if "paragraphs" in section:
                    text+=section["paragraphs"]
                    text+=" "
            tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
            words=[word for word in tokens if word.isalnum()]
            filtered_tokens=[]
            for token in words:
                if re.search('[a-zA-Z]', token):
                    if re.sub(r"\b[a-zA-Z]\b", "", token):
                        filtered_tokens.append(token)
            stop_words = set(stopwords.words('english'))   
            filtered_words = [w for w in filtered_tokens if not w in stop_words]
            final_sent=" ".join(filtered_words)
            content.append(final_sent)
        for doc in newDF["title"]:
            titles.append(doc)
        return content,titles

    @classmethod
    def spacyAlgo(cls,content,titles):
        nlp = en_core_web_sm.load()
        Total_Persons=[]
        Total_Places=[]
        person_place_category=[]
        for cont in range(len(content)):
            doc=nlp(content[cont])
            final={"Doc":content[cont],"Person":[],"Place":[],"Title":titles[cont]}
            for X in doc.ents:
                if X.label_=="GPE":
                    Total_Places.append(X.text)
                    final["Place"].append(X.text)
                elif X.label_=="PERSON":
                    Total_Persons.append(X.text)
                    final["Person"].append(X.text)
            person_place_category.append(final)
        return Total_Persons,Total_Places,person_place_category



    @classmethod
    def freqDist(cls,person_place_category,Distinct_total_persons,Distinct_total_places):
        person_format={"Name":[],"Doc_count":[]}
        place_format={"Name":[],"Doc_count":[]}
        for doc in person_place_category:
            for person in Distinct_total_persons:
                if person in doc["Person"]:
                    if person in person_format["Name"]:
                        person_format["Doc_count"][person_format["Name"].index(person)]+=1
                    else:
                        person_format["Name"].append(person)
                        person_format["Doc_count"].append(1)
            for place in Distinct_total_places:
                if place in doc["Place"]:
                    if place in place_format["Name"]:
                        place_format["Doc_count"][place_format["Name"].index(place)]+=1
                    else:
                        place_format["Name"].append(place)
                        place_format["Doc_count"].append(1)

        df_person_format=pd.DataFrame.from_dict(person_format)
        df_place_format=pd.DataFrame.from_dict(place_format)

        df_person_format.sort_values("Doc_count",inplace=True,ascending=False)
        df_person_format.reset_index(drop=True,inplace=True)

        df_place_format.sort_values("Doc_count",inplace=True,ascending=False)
        df_place_format.reset_index(drop=True,inplace=True)
        return df_person_format,df_place_format


    @classmethod
    def categorization(cls,person_place_category,df_person_format,df_place_format):
        person_categorization={"Cluster":[],"Doc_Number":[],"Title":[]}
        place_categorization={"Cluster":[],"Doc_Number":[],"Title":[]}
        for doc in range(len(person_place_category)):
            for person_name in df_person_format[:10]["Name"]:
                if person_name in person_place_category[doc]["Person"]:
                    person_categorization["Cluster"].append(person_name)
                    person_categorization["Doc_Number"].append(doc)
                    person_categorization["Title"].append(person_place_category[doc]["Title"])
            for place_name in df_place_format[:10]["Name"]:
                if place_name in person_place_category[doc]["Place"]:
                    place_categorization["Cluster"].append(place_name)
                    place_categorization["Doc_Number"].append(doc)
                    place_categorization["Title"].append(person_place_category[doc]["Title"])
        return person_categorization,place_categorization