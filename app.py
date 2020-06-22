import gspread
import os

from dotenv import load_dotenv
load_dotenv()

from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("iGEM GitHub Repo Automation Test (Responses)").sheet1

data = sheet.get_all_records()

GitToken = os.getenv('TOKEN')
username = 'ryu-bu'

newCell = 'added'
count = 2
checkIfAdded = False
for i in data:
    if not (i['Status']):
        name = i['PROJECT_NAME']
        collab = i['GITHUB_ID']

        newRepo = 'git@github.com:ryu-bu/' + name
        os.system('curl -H \"Authorization: token ' + GitToken + '\" --data \'{\"name\":\"' + name + '\"}\' https://api.github.com/user/repos')
        os.system('curl -H \"Authorization: token ' + GitToken + '\" \"https://api.github.com/repos/' + username + '/' + name
                    + '/collaborators/' + collab + '\" -X PUT -d \'{\"permission\":\"admin\"}\'')

        sheet.update_cell(count, 4, 'added')
        checkIfAdded = True


    count = count + 1

if not (checkIfAdded):
    print('Nothing New')
