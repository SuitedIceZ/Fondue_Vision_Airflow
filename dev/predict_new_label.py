from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
from dotenv import dotenv_values
# Load environment variables from .env file
env_vars = dotenv_values()

input_path = env_vars['FILE_BUFFER_PATH'] + 'raw_data.csv'

th2en = Translate('th', 'en')
nlp = spacy_sentence_bert.load_model('en_stsb_distilbert_base')

model = joblib.load(env_vars['FILE_MODELS_PATH'] + 'svc_model.pkl')

print("model loaded")

def predict(input):
    translated = th2en.translate(input)
    print("translated: from ",input," to -> ",translated)
    vector = nlp(translated).vector
    result = model.predict([vector])
    print("test type ",result[0])
    return result[0]

predict("ฝนตกหนักน้ำท่วมสูง น้ำนองเปียก")
predict("แมวหมาเต็มไปหมด")
predict("สกปรกมาก ส่งกลิ่นเหม็น")
predict("หลอดไฟแตก มืดมากๆ")
predict("ถนนร้าว เป็นหลุมเป็นบ่อ")
predict("มีคนจร มานอนเยอะมาก")


