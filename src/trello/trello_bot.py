# src/trello/trello_bot.py

from .trello_api import TrelloClient

# Temporary dictionary to store Trello card to Google Calendar event ID mapping
card_event_map = {}

class TrelloBot:
    def __init__(self):
        self.trello_client = TrelloClient()

    # Example method showing how the bot could use the TrelloClient
    def add_card_and_map_event(self, card_name: str, list_name: str, event_id: str):
        card = self.trello_client.add_card_to_trello(card_name, list_name)
        card_id = card.get('id')
        if card_id:
            card_event_map[card_id] = event_id
            return card_id
        return None