# src/trello/trello_api.py
import os
import requests
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Environment variables
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')

# Base URL for Trello API
TRELLO_API_BASE = "https://api.trello.com/1"


class TrelloClient:
    def __init__(self, api_key: str = TRELLO_API_KEY, token: str = TRELLO_TOKEN, board_id: str = TRELLO_BOARD_ID):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id

    def get_trello_list_id(self, list_name: str, include_archived: bool = False) -> Optional[str]:
        """
        Fetch a Trello list ID by name.
        """
        filter_value = 'all' if include_archived else 'open'
        lists_url = f"{TRELLO_API_BASE}/boards/{self.board_id}/lists"
        params = {
            'key': self.api_key,
            'token': self.token,
            'filter': filter_value
        }
        response = requests.get(lists_url, params=params)
        if response.status_code == 200:
            lists = response.json()
            for lst in lists:
                if lst['name'].lower() == list_name.lower():
                    return lst['id']
            return None
        else:
            raise Exception(f"Failed to fetch lists from Trello: {response.status_code}, {response.text}")

    def create_trello_list(self, list_name: str) -> str:
        """
        Create a new Trello list.
        """
        create_list_url = f"{TRELLO_API_BASE}/boards/{self.board_id}/lists"
        params = {
            'key': self.api_key,
            'token': self.token,
            'name': list_name,
            'pos': 'bottom'
        }
        response = requests.post(create_list_url, params=params)
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise Exception(f"Failed to create list '{list_name}': {response.status_code}, {response.text}")

    def add_card_to_trello(self, card_name: str, list_name: str, due_date: str = None) -> dict:
        """
        Add a card to a specified Trello list with an optional due date.
        """
        list_id = self.get_trello_list_id(list_name)
        if list_id is None:
            # List does not exist, so create it
            list_id = self.create_trello_list(list_name)

        create_card_url = f"{TRELLO_API_BASE}/cards"
        params = {
            'key': self.api_key,
            'token': self.token,
            'idList': list_id,
            'name': card_name,
            'due': due_date
        }
        response = requests.post(create_card_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to add card to Trello: {response.status_code}, {response.text}")

    def get_trello_cards(self, list_name: str) -> list:
        """
        Fetch all cards from a specified Trello list.
        """
        list_id = self.get_trello_list_id(list_name)
        if list_id is None:
            raise Exception(f"The list '{list_name}' does not exist in Trello.")

        get_cards_url = f"{TRELLO_API_BASE}/lists/{list_id}/cards"
        params = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.get(get_cards_url, params=params)
        
        if response.status_code == 200:
            cards = response.json()
            return cards
        else:
            raise Exception(f"Failed to fetch tasks from Trello: {response.status_code}, {response.text}")

    def delete_card_from_trello(self, card_name: str, list_name: str) -> Optional[str]:
        """
        Delete a card from a specified Trello list by name.
        """
        list_id = self.get_trello_list_id(list_name)
        if list_id is None:
            return None

        get_cards_in_list_url = f"{TRELLO_API_BASE}/lists/{list_id}/cards"
        params = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.get(get_cards_in_list_url, params=params)

        if response.status_code == 200:
            cards = response.json()
            for card in cards:
                if card['name'].lower() == card_name.lower():
                    card_id = card['id']
                    delete_card_url = f"{TRELLO_API_BASE}/cards/{card_id}"
                    delete_response = requests.delete(delete_card_url, params=params)
                    
                    if delete_response.status_code == 200:
                        return card_id
                    else:
                        raise Exception(f"Failed to delete card: {delete_response.status_code}, {delete_response.text}")
            return None
        else:
            raise Exception(f"Failed to fetch tasks from Trello: {response.status_code}, {response.text}")

    def archive_trello_list(self, list_name: str) -> bool:
        """
        Archive a Trello list by its name.
        """
        list_id = self.get_trello_list_id(list_name, include_archived=True)
        if list_id is None:
            return False

        archive_list_url = f"{TRELLO_API_BASE}/lists/{list_id}/closed"
        params = {
            'key': self.api_key,
            'token': self.token,
            'value': 'true'
        }
        response = requests.put(archive_list_url, params=params)

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to archive the list '{list_name}': {response.status_code}, {response.text}")

    def get_card_id(self, card_name: str, list_name: str) -> Optional[str]:
        """
        Get the ID of a card by its name and the name of the list it is in.
        """
        list_id = self.get_trello_list_id(list_name)
        if list_id is None:
            return None

        cards_url = f"{TRELLO_API_BASE}/lists/{list_id}/cards"
        params = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.get(cards_url, params=params)

        if response.status_code == 200:
            cards = response.json()
            for card in cards:
                if card['name'].lower() == card_name.lower():
                    return card['id']
            return None
        else:
            raise Exception(f"Failed to fetch cards from Trello: {response.status_code}, {response.text}")

    def create_checklist_in_card(self, card_id: str, checklist_name: str) -> dict:
        """
        Create a checklist in a specified Trello card.
        """
        create_checklist_url = f"{TRELLO_API_BASE}/checklists"
        params = {
            'key': self.api_key,
            'token': self.token,
            'idCard': card_id,
            'name': checklist_name
        }
        response = requests.post(create_checklist_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create checklist: {response.status_code}, {response.text}")

    def get_checklist_id(self, card_id: str, checklist_name: str) -> Optional[str]:
        """
        Get the ID of a checklist by its name and the card ID it is in.
        """
        card_checklists_url = f"{TRELLO_API_BASE}/cards/{card_id}/checklists"
        params = {
            'key': self.api_key,
            'token': self.token
        }
        response = requests.get(card_checklists_url, params=params)

        if response.status_code == 200:
            checklists = response.json()
            for checklist in checklists:
                if checklist['name'].lower() == checklist_name.lower():
                    return checklist['id']
            return None
        else:
            raise Exception(f"Failed to fetch checklists from Trello: {response.status_code}, {response.text}")

    def add_item_to_checklist(self, checklist_id: str, item_name: str) -> dict:
        """
        Add an item to a specified Trello checklist.
        """
        add_checkitem_url = f"{TRELLO_API_BASE}/checklists/{checklist_id}/checkItems"
        params = {
            'key': self.api_key,
            'token': self.token,
            'name': item_name,
            'checked': 'false'
        }
        response = requests.post(add_checkitem_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to add item to checklist: {response.status_code}, {response.text}")