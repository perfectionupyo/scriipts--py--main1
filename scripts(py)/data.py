from google.oauth2 import service_account
from googleapiclient.discovery import build

class Sheeter:
    def __init__(self):
        self.sheet_id = '1fqxuTjNpp5L2MuguLKNlUt4LKlR-RX0UkvJHQLb-XU0'
        self.service = build('sheets', 'v4', credentials=service_account.Credentials.from_service_account_file('scripts(py)/creds.json'))

    def append_to_sheet(self, range_, values):#write to the motherfucking spreadsheet
    # Call the 'values().append()' method to append the new data to the sheet.
        request_body = {
            'range': range_,
            'values': values,
            'majorDimension': 'ROWS',
        }
        response = self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=range_,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=request_body,
        ).execute()
    
    def call_func_to_write(self, here, user_data):
        keys = ['user_id', 'age', 'bad', 'minus', 'gender', 'weight', 'height', 'BMI', 'goal', 'new', 'gym']
        if here:
            temp = []
            for i in range(4):
                temp.append(user_data[keys[i]])
            self.append_to_sheet("Sheet!A:D", temp)

        elif not here:
            temp = []
            for i in keys:
                temp.append(user_data[i])


if __name__ == '__main__':
    x = {'user_id':None, 'age':None, 'bad':None, 'minus':None, 'gender':None, 'weight':0, 'height':0, 'BMI':0, 'goal':None, 'new':None, 'gym':None}
    nigga = Sheeter()
    nigga.call_func_to_write(True, x)