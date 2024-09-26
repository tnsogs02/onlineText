from flask import render_template, Response, request
import json
from app.services.ai_category import AiCategory
from app.services.google_sheets import GoogleSheets

def index():
    google_sheets = GoogleSheets()
    service_account_email = google_sheets.get_service_account_email()
    return render_template("index.html", service_account_email=service_account_email)

def check_sheet_available():
    try:
        google_sheets = GoogleSheets()
        ai_category = AiCategory()
        data = request.json
        sheet_url = str(data['sheetUrl'])
        sheet_object = google_sheets.open_by_url(sheet_url)
        return Response(response=json.dumps({
            'success': True,
            'message': "",
            'tabName': [i.title for i in sheet_object.worksheets()],
            'processorName': ai_category.get_available_processors()
        }), status=200)
    except:
        return Response(response=json.dumps({'success': False, 'message': "Failed to check availability of this sheet"}), status=500)
    
def run_predict():
    try:
        google_sheets = GoogleSheets()
        ai_category = AiCategory()
        data = request.values
        current_spreadsheet = google_sheets.open_by_url(data["google_doc_url"])
        current_worksheet = current_spreadsheet.worksheet_by_title(data["tab_name"])
        return_dataframe = ai_category.run_predict(data["processor_name"], google_sheets.get_sheet_as_df(current_worksheet))
        if(len(return_dataframe) > 0):
            current_worksheet.clear()
            current_worksheet.set_dataframe(return_dataframe, (1, 1), fit = True)
            return render_template("finish_predict.html", sheet_url=data["google_doc_url"])
    except:
        return Response(response=json.dumps({'success': False, 'message': "Caught error when trying to predict categories"}), status=500)