import os.path
import datetime as dt
from datetime import timedelta, datetime

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = service_account.Credentials.from_service_account_file(
    filename='credentials.json', scopes=SCOPES
)
service = build('calendar', 'v3', credentials=creds)
load_dotenv()


async def read_all_date_google():
    try:
        now = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
        thirty_days_later = (dt.datetime.now() + timedelta(days=30)).isoformat() + "Z"

        # Получаем все события в заданном интервале
        event_results = service.events().list(
            calendarId=os.getenv('CALENDAR_ID'),
            timeMin=now,
            timeMax=thirty_days_later,
            singleEvents=True,
            orderBy="startTime"
        )
        events = event_results.execute().get("items", [])

        all_dates = set()

        # Записываем все даты во множество
        for event in events:
            start = event["start"].get("dateTime", event['start'].get('date'))
            # Обновите формат, учитывая, что это может быть только дата
            date = dt.datetime.strptime(start.split('T')[0], "%Y-%m-%d").date()
            all_dates.add(date)

        # Получаем все даты на 30 дней вперед
        all_dates_in_30_days = [dt.datetime.now().date() + timedelta(days=x) for x in range(30)]

        # Находим даты, в которых нет событий
        dates_without_events = sorted(set(all_dates_in_30_days) - all_dates)

        return dates_without_events

    except HttpError as error:
        print(f"This error: {error}")
        return []


async def insert_new(count, height, material, address, phone, date,
                     zapil_quantity_v_google, zapil_quantity_k_google,
                     zapil_quantity_m_google, freight_elevator_google, sealing_uniq_google, sealing_up_google,
                     user_id_google, comment_google, name_google, floor_type_google, recognize_us_google, consumables_g,
                     mdf_color, material_sign):

    try:

        # event_date уже является объектом datetime.date
        event_date = date

        # Определяем время начала и конца события
        start_time = datetime(event_date.year, event_date.month, event_date.day, 7, 0)
        end_time = datetime(event_date.year, event_date.month, event_date.day, 17, 0)

        # Формируем тело события

        if material_sign == 'Панели':
            event_body = {
                "summary": f"{user_id_google}",
                "description": f"{name_google}\n{floor_type_google}\n\n{count}\n{height}\n"
                               f"{freight_elevator_google}\n{consumables_g}\n"
                               f"{material}\n{address}\n{phone}\n{recognize_us_google}\n{comment_google}",
                "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"}
            }
        else:
            event_body = {
                "summary": f"{user_id_google}",
                "description": f"{name_google}\n{floor_type_google}\n"
                               f"{mdf_color}\n{count}\n{height}\n{zapil_quantity_v_google}\n{zapil_quantity_k_google}\n"
                               f"{zapil_quantity_m_google}\n"
                               f"{sealing_up_google}\n{sealing_uniq_google}\n{freight_elevator_google}\n{consumables_g}\n"
                               f"{material}\n{address}\n{phone}\n{recognize_us_google}\n{comment_google}",
                "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"}
            }

        # Создаем событие
        event = service.events().insert(
            calendarId=os.getenv('CALENDAR_ID'),
            body=event_body
        ).execute()

        print(f"Event created: {event['id']}")

    except HttpError as error:
        print(f"This error: {error}")


async def get_tomorrows_event():
    try:

        # Определение времени начала и конца завтрашнего дня
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)
        end_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59)

        # Формирование запроса календаря для получения событий завтрашнего дня
        events_result = service.events().list(
            calendarId=os.getenv('CALENDAR_ID'),
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            maxResults=1,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            print("No events found for tomorrow.")
        else:
            for event in events:
                return event['summary']

    except HttpError as error:
        print(f"This error: {error}")


