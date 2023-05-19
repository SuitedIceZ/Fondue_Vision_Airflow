
# Install
## apt-get
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 python3-pip python3-venv
```
## set python airflow virtual environment 
```
python3 -m venv airflow_venv
```
## Activate
```
source airflow_venv/bin/activate
```
## install python dependency
### Airflow
```
pip install --upgrade apache-airflow[postgres,ssh,celery]
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib google-auth google-auth-oauthlib
pip install --upgrade python-dotenv pandas
pip install pythainlp[translate]
pip install spacy_sentence_bert
pip install tensorboardX
pip install uvicorn
```
### Service
```
sudo apt install uvicorn 
pip install fastapi
```

# Init
## Initialize airflow
```
airflow db init
```
## create user
```
airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email example@example.com
```

# Run
## airflow
```
airflow webserver -p 8080
```

```
airflow scheduler
```
## service
```
uvicorn main:app 
```

