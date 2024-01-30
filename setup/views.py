
import os.path


from blog.models import Post, Post_Comment, Post_Category, Post_Tag
from django.shortcuts import render

from calendario.quickstart.quickstart import credentials

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_free_slots():
    # Autenticação e configuração da API (omitido para brevidade)
    creds = credentials()

    service = build("calendar", "v3", credentials=creds)

    # Define o período de consulta
    now = datetime.datetime.utcnow()
    end_date = now + datetime.timedelta(days=60)

    # Consulta a API do Google Calendar
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
    events = events_result.get("items", [])

    # Filtra os eventos 'livres'
    free_slots = []
    for event in events:
        if event.get("summary").lower() == "livre":
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            free_slots.append({"start": start, "end": end})

    return free_slots

# Exemplo de chamada da função


import pytz

def format_slot(slot):
    # Define o formato desejado
    formato = "%d-%b-%Y às %H:%M"

    # Converte as strings de data/hora para objetos datetime
    start_dt = datetime.datetime.fromisoformat(slot['start'])
    end_dt = datetime.datetime.fromisoformat(slot['end'])

    # Se necessário, ajusta o fuso horário para o local (exemplo: 'America/Sao_Paulo')
    timezone = pytz.timezone('America/Sao_Paulo')
    start_dt_local = start_dt.astimezone(timezone)
    end_dt_local = end_dt.astimezone(timezone)

    # Formata as datas/horas
    start_formatted = start_dt_local.strftime(formato)
    end_formatted = end_dt_local.strftime("%H:%M")  # Não precisa repetir a data

    return f"{start_formatted}"

def home(request):

    # free_slots = get_free_slots()
    # formatted_slots = [format_slot(slot) for slot in free_slots]
    # print('formatted_slots',formatted_slots)
    return render(request, 'index.html' )
