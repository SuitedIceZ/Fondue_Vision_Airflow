from fastapi import FastAPI, File, UploadFile, Form
from pythainlp.translate import Translate
import spacy_sentence_bert
from pydantic import BaseModel
import joblib
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


th2en = Translate('th', 'en')
nlp = spacy_sentence_bert.load_model('en_stsb_distilbert_base')

model = joblib.load(env_vars['FILE_MODELS_PATH'] + 'svc_model_2.pkl')

class Text(BaseModel):
    input: str

@app.get("/")
async def test():
    return {"message": "Hello World"}

@app.post("/predict/text")
async def predict_text(text:Text):
    translated = th2en.translate(text.input)
    vector = nlp(translated).vector
    result = model.predict([vector])
    #print(test,result[0])
    return {"type": result[0]}