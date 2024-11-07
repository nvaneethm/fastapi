# core/load_data.py

import json
from app.models import JiraTicket

def load_jira_tickets(filepath: str = "app/data/jira_tickets.json") -> list:
    with open(filepath, "r") as f:
        data = json.load(f)
    return [JiraTicket(**ticket) for ticket in data]
