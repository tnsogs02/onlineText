import pygsheets

class GoogleSheets():
    def __init__(self, token_path='app/tokens/googlesheets_token.json'):
        self.auth = pygsheets.authorize(service_account_file=token_path)
        
    def get_service_account_email(self):
        return self.auth.oauth.service_account_email
        
    def open_by_url(self, sheet_url):
        return self.auth.open_by_url(sheet_url)
        
    def get_sheet_as_df(self, worksheet):
        dataframe = worksheet.get_as_df(include_tailing_empty = False)
        return dataframe