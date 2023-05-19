from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
from dotenv import dotenv_values
import csv
import requests
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'tokenized_data.csv'

def relabel_data():
    # load data
    data_dict = []
    with open(input_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data_dict.append(row)

    # predict and relabel all rows
    for i in range(len(data_dict)):
        data = {
            "input": data_dict[i][2]
        }
        # res = requests.post(f"http://localhost:8000/predict/text")
        response = requests.post("http://localhost:8000/predict/text", json=data)
        data_dict[i][7] = response.text.split('"')[3]
        if(i%1000==0):
            print(i/len(data_dict)*100, "%")

    #write data to csv
    csv_columns = ['type','Name','description','photo_url','timestamp','state','tokenized_description','new_label']
    csv_file_output = env_vars['FILE_BUFFER_PATH'] + "relabeled_data.csv"
    with open(csv_file_output, 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(csv_columns)
        write.writerows(data_dict)
