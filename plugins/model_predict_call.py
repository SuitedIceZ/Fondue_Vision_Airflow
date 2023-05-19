from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
from dotenv import dotenv_values
import csv
import requests
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'tokenized_data.csv'
isStopAt100 = True

def relabel_data():
    # load data
    data_dict = []
    with open(input_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data_dict.append(row)

    # label translation
    dictionary_list = [('สัตว์จรจัด', 'stray'),
        ('ความสะอาด', 'sanitary'),
        ('ป้าย', 'sign'),
        ('คนจรจัด', 'homeless'),
        ('ทางเท้า', 'sidewalk'),
        ('ต้นไม้', 'tree'),
        ('ความปลอดภัย', 'safety'),
        ('ถนน', 'roads'),
        ('ท่อระบายน้ำ', 'sewer'),
        ('น้ำท่วม', 'flooding'),
        ('สะพาน', 'bridge'),
        ('เสียงรบกวน', 'noise'),
        ('PM2.5', 'PM2.5'),
        ('แสงสว่าง', 'light'),
        ('จราจร', 'traffic'),
        ('เสนอแนะ', 'etc'),
        ('กีดขวาง', 'obstacle'),
        ('สายไฟ', 'electric'),
        ('ร้องเรียน', 'complaint'),
        ('คลอง', 'canal'),
        ('สอบถาม', 'question'),
        ('การเดินทาง', 'travel'),
        ('ป้ายจราจร', 'traffic sign'),
        ('ห้องน้ำ', 'toilet')]

    th2en_label_dictionary = {}
    en2th_label_dictionary = {}
    for i in range(len(dictionary_list)):
        #print(dictionary_list[i][0])
        th2en_label_dictionary[dictionary_list[i][0]] = dictionary_list[i][1]
        en2th_label_dictionary[dictionary_list[i][1]] = dictionary_list[i][0]
    print("th2en dict",th2en_label_dictionary)
    print("en2th dict",en2th_label_dictionary)

    # set default new_label to first of column 0
    for i in range(len(data_dict)):
        data_dict[i][7] = data_dict[i][0].split(',')[0]
        
    # predict and relabel all rows
    for i in range(len(data_dict)):
        data = {
            "input": data_dict[i][2]
        }
        # res = requests.post(f"http://localhost:8000/predict/text")
        response = requests.post("http://localhost:8000/predict/text", json=data)
        data_dict[i][7] = response.text.split('"')[3]
        # print("test response :",data_dict[i][7], response.text.split('"')[3])
        # translate new_label back to thai
        
        # print("test before :", data_dict[i][7])
        data_dict[i][7] = en2th_label_dictionary[data_dict[i][7]]
        # print("test after :", data_dict[i][7])
        if(i%100==0):
            print(i/len(data_dict)*100, "%", " writing back up to csv")
            #write data to csv
            csv_columns = ['type','longitude','description','photo_url','timestamp','state','tokenized_description','new_label','latitude']
            csv_file_output = env_vars['FILE_BUFFER_PATH'] + "relabeled_data.csv"
            with open(csv_file_output, 'w') as csvfile:
                write = csv.writer(csvfile)
                write.writerow(csv_columns)
                write.writerows(data_dict)
            
            if(i != 0 and isStopAt100):
                break

    #write data to csv
    csv_columns = ['type','longitude','description','photo_url','timestamp','state','tokenized_description','new_label','latitude']
    csv_file_output = env_vars['FILE_BUFFER_PATH'] + "relabeled_data.csv"
    with open(csv_file_output, 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(csv_columns)
        write.writerows(data_dict)
