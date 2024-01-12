""" The following code is for the Google Form service. You can use this to submit data to a Google Form. """
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "static/cogito-website-backend-secret-key.json", scopes
)


def get_all_applications():
    """Returns all applications"""
    file = gspread.authorize(credentials)
    sheet_name = "Prosjektsøknad 2024 Vår (Responses)"
    worksheet = file.open(sheet_name)
    sheet = worksheet.sheet1
    return sheet.get_all_records()


def submit_application_to_google_form(data: list):
    """Submits an application to the Google Form"""
    sheet.insert_row(data, 1)

    file = gspread.authorize(credentials)
    sheet_name = "Prosjektsøknad 2024 Vår (Responses)"
    worksheet = file.open(sheet_name)
    sheet = worksheet.sheet1
    sheet.insert_row(data, 1)


if __name__ == "__main__":
    data = get_all_applications()
    print(data)
