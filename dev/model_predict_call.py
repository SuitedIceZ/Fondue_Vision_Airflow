from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
from dotenv import dotenv_values
import csv
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'tokenized_data.csv'

def main():
    # load model
    th2en = Translate('th', 'en')
    nlp = spacy_sentence_bert.load_model('en_stsb_distilbert_base')
    model = joblib.load(env_vars['FILE_MODELS_PATH'] + 'svc_model.pkl')
    print("model loaded")

    # load data
    data_dict = []
    with open(input_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data_dict.append(row)

    # predict and relabel all rows
    for i in range(len(data_dict)):
        translated = th2en.translate(data_dict[i][2])
        vector = nlp(translated).vector
        result = model.predict([vector])
        data_dict[i][7] = result[0]
        if(i%1000==0):
            print(i/len(data_dict)*100, "%")
        if(i==10):
            break # for testing

    #write data to csv
    csv_columns = ['type','Name','description','photo_url','timestamp','state','tokenized_description','new_label']
    csv_file_output = env_vars['FILE_BUFFER_PATH'] + "relabeled_data.csv"
    with open(csv_file_output, 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(csv_columns)
        write.writerows(data_dict)

if __name__ == "__main__":
    main()

