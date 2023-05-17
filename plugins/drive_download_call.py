from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import io
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values()

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# buffer_full_path = '/home/natnaphon/airflow/file_buffer/'
buffer_full_path = env_vars['FILE_BUFFER_PATH']

def download_from_drive():
    filename = 'MyReport.csv'
    # Replace 'MyReport.csv' with filename , later add in parameter

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(buffer_full_path+'token.pickle'):
        with open(buffer_full_path+'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                buffer_full_path+'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(buffer_full_path+'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API to find the file
    results = service.files().list(
        q="name = 'MyReport.csv'", spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            file_id = item['id']
            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO(buffer_full_path+'destination2.csv', 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

    # Replace 'FILE_ID' with your file's id
    # file_id = '1wJ74U0pvTw6zKVZLr2A2w41uFk9PtHmouqSevKaD2mg'
    # file_id = '1ginGM5qfEli0KkXi2bTQUnP2Ci8iX4ro'
    # request = service.files().get_media(fileId=file_id)
    # fh = io.FileIO(buffer_full_path+'destination.csv', 'wb')
    # downloader = MediaIoBaseDownload(fh, request)
    # done = False
    # while done is False:
    #     status, done = downloader.next_chunk()
    #     print("Download %d%%." % int(status.progress() * 100))
