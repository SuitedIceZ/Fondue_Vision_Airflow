import os.path
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload 
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values()

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
# root_full_path = '/home/natnaphon/airflow/file_buffer/'
buffer_full_path = env_vars['FILE_BUFFER_PATH']

def main():
    filename = 'MyReport.csv'
    folder_id = env_vars['DRIVE_FOLDER_ID']
    # The existing code in your main function goes here
    # Replace 'MyReport.csv' with filename , later add in parameter
    # Replace 'TARGET_DIRECTORY_ID' with folder_id , later add in parameter
    creds = None
    if os.path.exists(buffer_full_path+'token.pickle'):
        with open(buffer_full_path+'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                buffer_full_path+'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(buffer_full_path+'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API to upload the csv file
    file_metadata = {
        'name': 'MyReport.csv',
        'parents': ['1TU3oUUjU72i4rHDt6XAMqYOP1Pqbdh76']
    }
    media = MediaFileUpload(buffer_full_path+'MyReport.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    main()
