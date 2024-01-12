""" The following code is for the Google Form service. You can use this to submit data to a Google Form. """
from dataclasses import dataclass, asdict
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@dataclass(frozen=True)
class Credentials:
    """Credentials for Google Form"""

    load_dotenv()

    type: str = os.getenv("GOOGLE_API_TYPE")
    project_id: str = os.getenv("GOOGLE_API_PROJECT_ID")
    private_key_id: str = os.getenv("GOOGLE_API_PRIVATE_KEY_ID")
    private_key: str = os.getenv("GOOGLE_API_PRIVATE_KEY")
    client_email: str = os.getenv("GOOGLE_API_CLIENT_EMAIL")
    client_id: str = os.getenv("GOOGLE_API_CLIENT_ID")
    auth_uri: str = os.getenv("GOOGLE_API_AUTH_URI")
    token_uri: str = os.getenv("GOOGLE_API_TOKEN_URI")
    auth_provider_x509_cert_url: str = os.getenv(
        "GOOGLE_API_AUTH_PROVIDER_X509_CERT_URL"
    )
    client_x509_cert_url: str = os.getenv("GOOGLE_API_CLIENT_X509_CERT_URL")
    universe_domain: str = os.getenv("GOOGLE_API_UNIVERSE_DOMAIN")


def get_credentials():
    """Returns the credentials for the Google Form"""
    secrets = asdict(Credentials())
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(secrets, scopes)
    return credentials


def get_all_applications():
    """Returns all applications"""
    file = gspread.authorize(get_credentials())
    sheet_name = "Prosjektsøknad 2024 Vår (Responses)"
    worksheet = file.open(sheet_name)
    sheet = worksheet.sheet1
    return sheet.get_all_records()


def submit_application_to_google_form(data: list):
    """Submits an application to the Google Form

    Args:
        data (list): The data to be submitted. This should be a list of strings where each string is a column in the Google Form.
    """

    file = gspread.authorize(get_credentials())
    sheet_name = "Prosjektsøknad 2024 Vår (Responses)"
    worksheet = file.open(sheet_name)
    sheet = worksheet.sheet1
    sheet.insert_row(data, 1)


if __name__ == "__main__":
    data = get_all_applications()
    print(data)
