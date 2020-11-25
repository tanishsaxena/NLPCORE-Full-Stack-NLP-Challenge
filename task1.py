# Import libraries
import pandas as pd
import os
import json

#Working Class
class task1:
    def __init__(self,link):
        self.newDF=task1.data(link)
    def main(self):
        newDF=self.newDF
        data={"Attribute":[],"Freq":[],"Occur":[],"doc":[]}
        for doc in range(len(newDF["sections"])):
            for section in newDF["sections"][doc]:
                if "attributes" in section:
                    for attr in section["attributes"]:
                        if "name" in attr:
                            if attr["name"].lower().strip() in data["Attribute"]:
                                data["Freq"][data["Attribute"].index(attr["name"].lower().strip())]+=1
                                if data["doc"][data["Attribute"].index(attr["name"].lower().strip())]!=doc:
                                    data["Occur"][data["Attribute"].index(attr["name"].lower().strip())]+=1
                                    data["doc"][data["Attribute"].index(attr["name"].lower().strip())]=doc
                            else:
                                data["Attribute"].append(attr["name"].lower().strip())
                                data["Freq"].append(1)
                                data["Occur"].append(1)
                                data["doc"].append(doc)
        result=pd.DataFrame(data)
        result=result.sort_values("Occur",ascending=False)
        result.drop(['doc'], axis = 1, inplace=True)
        return result

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

