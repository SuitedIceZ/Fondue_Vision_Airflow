import os
from dotenv import dotenv_values
from pythainlp.tokenize import word_tokenize
# Load environment variables from .env file
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'raw_data.csv'

import csv
data_dict = []

def preprocess_data():
    with open(input_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data_dict.append(row)

    # print size of data_dict
    print("total data:",len(data_dict))

    data_droped_empty_label = []
    # drop any column that is not needed (only keep 1,2,4,6,9,14)
    c = 0
    for i in range(len(data_dict)):
        # drop empty label
        if(data_dict[i][0]==""):
            continue
        data_droped_empty_label.append([data_dict[i][0], data_dict[i][1], data_dict[i][3].replace("\n"," "), data_dict[i][5], data_dict[i][8], data_dict[i][13],"",""])

    # print size of data_dict after drop empty label
    print("total data:",len(data_droped_empty_label))

    # tokenize the text in column 2
    for i in range(len(data_droped_empty_label)):
        data_droped_empty_label[i][6] = word_tokenize(data_droped_empty_label[i][2], engine="newmm", keep_whitespace=False)
        if(i%1000==0):
            print(i/len(data_droped_empty_label)*100, "%")  

    # transfrom location to long (column 1), lat (column 8)
    for i in range(len(data_droped_empty_label)):
        data_droped_empty_label[i][1] = data_droped_empty_label[i][1].replace("[","")
        data_droped_empty_label[i][1] = data_droped_empty_label[i][1].replace("]","")
        data_droped_empty_label[i][1] = data_droped_empty_label[i][1].replace("'","")
        data_droped_empty_label[i][1] = data_droped_empty_label[i][1].replace(" ","")
        location = data_droped_empty_label[i][1].split(",")
        data_droped_empty_label[i][1] = location[0]
        data_droped_empty_label[i].append(location[1])

    #write data to csv
    csv_columns = ['type','longitude','description','photo_url','timestamp','state','tokenized_description','new_label','latitude']
    csv_file_output = env_vars['FILE_BUFFER_PATH'] + "tokenized_data.csv"
    with open(csv_file_output, 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(csv_columns)
        write.writerows(data_droped_empty_label)