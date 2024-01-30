import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:

        now = datetime.datetime.utcnow()
        end_date = now + datetime.timedelta(days=60)

                # Call the Calendar API
        service = build("calendar", "v3", credentials=creds)

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now.isoformat() + "Z",
                timeMax=end_date.isoformat() + "Z",
                maxResults=100,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        print(creds)
        events = events_result.get("items", [])

        free_events = [event for event in events if event.get("summary").lower() == "livre"]

        if not free_events:
            print("No free slots found.")
            return

        for event in free_events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

  except Exception as e:
      print(f"An error occurred: {e}")



def credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    print(creds)
    return creds

if __name__ == "__main__":
  main()