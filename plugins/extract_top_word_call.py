from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
from dotenv import dotenv_values
import csv
import requests
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'relabeled_data.csv'

def extract_top_word():
    # define dictionary
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

    # load data
    data_dict = []
    with open(input_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data_dict.append(row)

    # count word frequency
    unconsider_word = [':','\\u200b','\\r','*','-','(',')','#','/','ทับ','มี','ไม่','ให้','มา','และ','การ','ที่','ใน','จะ','ได้','ผู้','ไป','ใช้','จาก','ว่า','อยู่','บน','เป็น','ก็','ครับ','ค่ะ',"แล้ว"]

    freq_word_dict = {}
    for i in range(len(dictionary_list)):
        freq_word_dict[dictionary_list[i][0]] = {}

    for i in range(len(data_dict)):
        label_class = data_dict[i][7]
        # empty label use type (column 0) instead
        if(label_class == ''):label_class = data_dict[i][0].split(',')[0]

        if label_class not in freq_word_dict:
            freq_word_dict[label_class] = {}

        tokenized_word = data_dict[i][6][1:-1].split(", ")
        for j in range(len(tokenized_word)):
            word = tokenized_word[j][1:-1]
            if(word in unconsider_word):continue
            if word not in freq_word_dict[label_class]:
                freq_word_dict[label_class][word] = 0

            freq_word_dict[label_class][word] += 1

    # sort word frequency
    sorted_freq_word_list = {}
    for label_class, word_dict in freq_word_dict.items():
        sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
        sorted_freq_word_list[label_class] = sorted_words

    # generate top word dictionary
    top_word_dict = []
    for i in range(len(sorted_freq_word_list)):
        # print("the label:",dictionary_list[i][0],"has",sorted_freq_word_list[dictionary_list[i][0]])
        top_word_dict.append([dictionary_list[i][0],sorted_freq_word_list[dictionary_list[i][0]][:10]])

    # convert top word dictionary to csv
    top_word_to_csv = []
    for i in range(len(top_word_dict)):
        for j in range(len(top_word_dict[i][1])):
            top_word_to_csv.append([top_word_dict[i][0],top_word_dict[i][1][j][0],top_word_dict[i][1][j][1]])



    #write data to csv
    csv_columns = ['type','word','count']
    csv_file_output = env_vars['FILE_BUFFER_PATH'] + 'top_word_data_by_word.csv'
    with open(csv_file_output, 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(csv_columns)
        write.writerows(top_word_to_csv)
