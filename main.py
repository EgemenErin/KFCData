import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time
import datetime
import os


# Function to authenticate and open Google Sheets
def upload_to_google_sheets(data):
    # Authenticate using the service account
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("screentime_data").sheet1

    # Insert the new data (appending to the sheet)
    sheet.append_row(data)


# Function to extract text from screen time images
def extract_screentime_data(image_folder):
    data = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img_path = os.path.join(image_folder, filename)
            img = Image.open(img_path)
            text = pytesseract.image_to_string(img)
            data.append(text)

    return data


# Function to process and upload daily screen time data
def process_and_upload():
    # Get today's date
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Path to data folder where data will be stored
    image_folder = "/Users/egemenerin/Documents/Data"

    # Extract screen time data from images
    extracted_data = extract_screentime_data(image_folder)
    google_sheet_data = [today] + extracted_data

    # Upload the data to Google Sheets
    upload_to_google_sheets(google_sheet_data)


# Schedule the function to run daily at 12 PM
schedule.every().day.at("12:00").do(process_and_upload)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
