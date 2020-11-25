# Import libraries
import pandas as pd
import os
import json
import nltk
import re
from sklearn import feature_extraction
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from nltk.corpus import stopwords
# nltk.download("stopwords") 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


#Main Class
class task2:
    
    def __init__(self,link):
        self.newDF=task2.data(link)
    
    def main(self):
        content,titles=task2.content_title(self.newDF)
        tf_idf=task2.tf_idf_mat(content)
        
        num_clusters=task2.elbow_value(tf_idf)
        km = KMeans(n_clusters=num_clusters)
        km.fit(tf_idf)
        clusters = km.labels_.tolist()
        
        result=[]
        for i in range(len(clusters)):
            result.append({"clusters":clusters[i], "content":content[i], "title":titles[i]})
        result=json.dumps(result)
        
        #Storing resultant data as json in directories
        with open('Database\\task2.json', 'w') as f:
            json.dump(result, f)
        
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
        return newDF[:50]
    
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
            stems = [stemmer.stem(t) for t in filtered_tokens]
            stop_words = set(stopwords.words('english'))   
            filtered_words = [w for w in stems if not w in stop_words]
            final_sent=" ".join(filtered_words)
            content.append(final_sent)
        for doc in newDF["title"]:
            titles.append(doc)
        return content,titles
    
    @classmethod
    def tf_idf_mat(cls,content):
        
        #define vectorizer parameters
        vectorizer = TfidfVectorizer(stop_words={'english'})
        tfidf_matrix = vectorizer.fit_transform(content)
        # terms = vectorizer.get_feature_names()
        return tfidf_matrix
    
    @classmethod
    def elbow_value(cls,tfidf_matrix):
        Sum_of_squared_distances = []
        K = range(2,10)
        for k in K:
            km = KMeans(n_clusters=k, max_iter=200, n_init=10)
            km = km.fit(tfidf_matrix)
            Sum_of_squared_distances.append(km.inertia_)
        return K[int(len(Sum_of_squared_distances)/2)]

#Main Condition
if __name__=="__main__":
    obj=task2("Data")
    obj.main()