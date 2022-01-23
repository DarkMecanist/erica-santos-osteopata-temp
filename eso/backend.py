import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import re


class GoogleCloudPlatform:
    """
    GoogleCloudPlatform

    Available Scopes:
     - Google Calendar: https://www.googleapis.com/auth/calendar

    """

    def __init__(self, api_name, api_version, scopes, client_secret_file):
        credentials = None
        pickle_file = f'token_{api_name}_{api_version}.pickle'
        temp_dir = os.path.join(os.getcwd(), ".temp")

        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        if os.path.exists(os.path.join(temp_dir, pickle_file)):
            with open(os.path.join(temp_dir, pickle_file), "rb") as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if os.path.exists(os.path.join(temp_dir, client_secret_file)):
                    flow = InstalledAppFlow.from_client_secrets_file(os.path.join(temp_dir, client_secret_file), scopes)
                    credentials = flow.run_local_server()
                else:
                    raise Exception(f"No file {client_secret_file} in dir {temp_dir}")

            with open(os.path.join(temp_dir, pickle_file), "wb") as token:
                pickle.dump(credentials, token)

        try:
            self.service = build(api_name, api_version, credentials=credentials)
            print(f"{api_name}, {api_version} service created successfully.")
        except Exception as e:
            os.remove(os.path.join(temp_dir, pickle_file))
            raise e


class GoogleCalendar(GoogleCloudPlatform):
    """
    Google Calendar API

    Available Scopes:
        "https://www.googleapis.com/auth/calendar"
    """

    def __init__(self, api_version):
        api_name = "calendar"
        scopes = ["https://www.googleapis.com/auth/calendar"]
        client_secret_file = "client_secret.json"
        super(GoogleCalendar, self).__init__(api_name, api_version, scopes, client_secret_file)

    def insert_event(self, summary, description, location, start_datetime, end_datetime,
                              attendee_emails, start_timezone="America/Los_Angeles", end_timezone="America/Los_Angeles",
                              recurrence_rules=None, reminders=None):
        """
        :param summary: [String]
        :param description: [String]
        :param location: [String]
        :param start_datetime: [DateTime]
        :param start_timezone: [String]
        :param end_datetime: [Datetime]
        :param end_timezone: [String]
        :param recurrence_rules: [List: String]
        :param attendee_emails: [List: String]
        :param reminders: [List: Dictionary]
        example reminders: [{"method": "email", "minutes": 30}, {"method": "popup", "minutes": 10}]
        :return: Dictionary
        """

        if not summary:
            raise Exception("Summary not provided.")

        if not description:
            raise Exception("Description not provided.")

        if not location:
            raise Exception("Location not provided.")

        if not start_datetime:
            raise Exception("Start DateTime nor provided.")

        if not end_datetime:
            raise Exception("End DateTime not provided.")

        if not attendee_emails:
            raise Exception("Attendee Emails not provided.")

        if not recurrence_rules:
            recurrence_rules = ["RRULE:FREQ=DAILY;COUNT=1"]

        if not reminders:
            reminders = [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10}
            ]

        event_info = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": f"{start_datetime.year}-{start_datetime.month}-{start_datetime.day}T"
                            f"{start_datetime.hour-1}:{start_datetime.minute}:00-00:00",
                "timeZone": start_timezone,
            },
            "end": {
                "dateTime": f"{end_datetime.year}-{end_datetime.month}-{end_datetime.day}T"
                            f"{end_datetime.hour-1}:{end_datetime.minute}:00-00:00",
                "timeZone": end_timezone,
            },
            "recurrence": recurrence_rules,
            "attendees": [{"email": email} for email in attendee_emails],
            "reminders": {
                "useDefault": False,
                "overrides": reminders
            }
        }

        event = self.service.events().insert(calendarId="primary", body=event_info).execute()

        print(f"Event created successfully ({event.get('htmlLink')})")

        return event


class Gmail:
    """Gmail methods"""

    def __init__(self, account_email, account_password):
        self.account_email = account_email
        self.account_password = account_password
        self.smtp_obj = smtplib.SMTP("smtp.gmail.com", 587)

    def send_email(self, emails_to, subject, body, attachments=[]):
        """
        :param emails_to: [List] emails to send
        :param subject: [String]
        :param body: [String]
        :param attachments: [List] file_paths
        """

        # Check emails_to not empty
        if len(emails_to) == 0:
            raise Exception("No emails provided.")

        # Check subject not empty
        if str(subject) == "":
            raise Exception("No subject provided.")

        # Check body not empty
        if str(body) == "":
            raise Exception("No body provided.")

        # Check if all emails are valid
        for email in emails_to:
            is_valid_email = Strings().is_valid_email(email)
            if not is_valid_email:
                raise Exception(f"{email} is not a valid email.")

        email_message = MIMEMultipart()
        email_message["From"] = self.account_email
        email_message["To"] = COMMASPACE.join(emails_to)
        email_message["Date"] = formatdate(localtime=True)
        email_message["Subject"] = subject
        email_message.attach(MIMEText(body))

        for attachment in attachments:
            with open(attachment, "rb") as file:
                part = MIMEApplication(file.read(), Name=basename(attachment))

            part["Content-Disposition"] = f'attachment; filename="{basename(attachment)}"'
            email_message.attach(part)

        with self.smtp_obj as sp:
            sp.ehlo()
            sp.starttls()
            sp.ehlo()
            sp.login(self.account_email, self.account_password)
            sp.sendmail(self.account_email, emails_to, email_message.as_string())


class Strings:
    """

        """

    def __init__(self):
        self.regex_email = "[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}"

    def is_valid_email(self, email):
        """
        :param email: [String]
        :return: [Boolean]

        Description: Checks if an the email string is a valid email format
        """

        if str(re.match(self.regex_email, email, re.IGNORECASE)) != "None":
            print(f"Email: {email} is valid.")
            return True
        else:
            print(f"Email: {email} is not valid.")
            return False