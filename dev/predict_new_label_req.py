from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
from dotenv import dotenv_values
import requests
# Load environment variables from .env file
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'raw_data.csv'

def predict(input):
    data = {
        "input": input
    }
    # res = requests.post(f"http://localhost:8000/predict/text")
    response = requests.post("http://localhost:8000/predict/text", json=data)
    print(response.text)
    print(response.text.split('"')[3])
    result = "temp"
    return result

predict("ฝนตกหนักน้ำท่วมสูง น้ำนองเปียก")
predict("แมวหมาเต็มไปหมด")
predict("สกปรกมาก ส่งกลิ่นเหม็น")
predict("หลอดไฟแตก มืดมากๆ")
predict("ถนนร้าว เป็นหลุมเป็นบ่อ")
predict("มีคนจร มานอนเยอะมาก")


