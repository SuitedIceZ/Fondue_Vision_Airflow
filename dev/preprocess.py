import os
from dotenv import dotenv_values
# Load environment variables from .env file
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'raw_data.csv'

import csv
data_dict = []

with open(input_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        data_dict.append(row)

# print size of data_dict
print("total data:",len(data_dict))

# drop any column that is not needed (only keep 1,2,4,6,9,14)
for i in range(len(data_dict)):
    data_dict[i] = [data_dict[i][0], data_dict[i][1], data_dict[i][3].replace("\n"," "), data_dict[i][5], data_dict[i][8], data_dict[i][13],""]
print(data_dict[0])
print(data_dict[0][2])


from pythainlp.tokenize import word_tokenize    

text = "โอเคบ่พวกเรารักภาษาบ้านเกิด"

print(word_tokenize(text, engine="newmm", keep_whitespace=False))

# tokenize the text in column 2
for i in range(len(data_dict)):
    data_dict[i][6] = word_tokenize(data_dict[i][2], engine="newmm", keep_whitespace=False)
    if(i%1000==0):
        print(i/len(data_dict)*100, "%")

#write data to csv
csv_columns = ['type','Name','description','photo_url','timestamp','state','tokenized_description']
csv_file_output = env_vars['FILE_BUFFER_PATH'] + "tokenized_data.csv"
with open(csv_file_output, 'w') as csvfile:
    write = csv.writer(csvfile)
    write.writerow(csv_columns)
    write.writerows(data_dict)