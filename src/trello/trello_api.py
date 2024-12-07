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

# Function to get a Trello list ID by name
def get_trello_list_id(list_name: str, include_archived: bool = False) -> Optional[str]:
    """
    Fetch a Trello list ID by name.

    Args:
        list_name (str): The name of the Trello list to fetch.
        include_archived (bool): Whether to include archived lists in the search. Defaults to False.

    Returns:
        Optional[str]: The Trello list ID if found, else None.

    Raises:
        Exception: If the lists cannot be fetched due to an API error.
    """
    # Fetch all lists (both open and closed if include_archived is True)
    filter_value = 'all' if include_archived else 'open'
    url_all_lists = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists"
    query_params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'filter': filter_value
    }
    response_all = requests.get(url_all_lists, params=query_params)

    if response_all.status_code == 200:
        lists = response_all.json()
        for lst in lists:
            if lst['name'].lower() == list_name.lower():
                return lst['id']
        # List not found
        return None
    else:
        raise Exception(f"Failed to fetch lists from Trello: {response_all.status_code}, {response_all.text}")
# Function to create a new Trello list
def create_trello_list(list_name: str) -> str:
    """
    Create a new Trello list.

    Args:
        list_name (str): The name of the Trello list to create.

    Returns:
        str: The Trello list ID.

    Raises:
        Exception: If the list cannot be created due to an API error.
    """
    create_list_url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'name': list_name,
        'pos': 'bottom'
    }
    create_response = requests.post(create_list_url, params=query)
    if create_response.status_code == 200:
        return create_response.json()['id']
    else:
        raise Exception(f"Failed to create list '{list_name}': {create_response.status_code}, {create_response.text}")

# Add a card to a specified list in Trello with an optional due date
def add_card_to_trello(card_name: str, list_name: str, due_date: str = None) -> dict:
    """
    Add a card to a specified Trello list with an optional due date.

    Args:
        card_name (str): The name of the card to add.
        list_name (str): The name of the Trello list to add the card to.
        due_date (str, optional): The due date for the card in ISO 8601 format. Defaults to None.

    Returns:
        dict: The created card's details.

    Raises:
        Exception: If the card cannot be added due to an API error.
    """
    list_id = get_trello_list_id(list_name)
    if list_id is None:
        # List does not exist, so create it
        list_id = create_trello_list(list_name)

    url = f"https://api.trello.com/1/cards"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': list_id,
        'name': card_name,
        'due': due_date  # Add due date to the query parameters
    }
    response = requests.post(url, params=query)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add card to Trello: {response.status_code}, {response.text}")

# Fetch Trello cards from a specified list
def get_trello_cards(list_name: str) -> list:
    """
    Fetch all cards from a specified Trello list.

    Args:
        list_name (str): The name of the Trello list to fetch cards from.

    Returns:
        list: A list of cards in the specified Trello list.

    Raises:
        Exception: If the cards cannot be fetched due to an API error.
    """
    list_id = get_trello_list_id(list_name)
    if list_id is None:
        raise Exception(f"The list '{list_name}' does not exist in Trello.")

    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    query_params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.get(url, params=query_params)
    
    if response.status_code == 200:
        cards = response.json()
        return cards
    else:
        raise Exception(f"Failed to fetch tasks from Trello: {response.status_code}, {response.text}")

# Delete a card from a specified list in Trello
def delete_card_from_trello(card_name: str, list_name: str) -> Optional[str]:
    """
    Delete a card from a specified Trello list by name.

    Args:
        card_name (str): The name of the card to delete.
        list_name (str): The name of the Trello list containing the card.

    Returns:
        Optional[str]: The ID of the deleted card, or None if the card was not found.

    Raises:
        Exception: If the card cannot be deleted due to an API error.
    """
    list_id = get_trello_list_id(list_name)
    if list_id is None:
        # List does not exist
        return None

    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    query_params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        cards = response.json()
        for card in cards:
            if card['name'].lower() == card_name.lower():
                card_id = card['id']
                delete_url = f"https://api.trello.com/1/cards/{card_id}"
                delete_query = {
                    'key': TRELLO_API_KEY,
                    'token': TRELLO_TOKEN
                }
                delete_response = requests.delete(delete_url, params=delete_query)
                
                if delete_response.status_code == 200:
                    return card_id
                else:
                    raise Exception(f"Failed to delete card: {delete_response.status_code}, {delete_response.text}")
        return None
    else:
        raise Exception(f"Failed to fetch tasks from Trello: {response.status_code}, {response.text}")

# Archive a Trello list by its name
def archive_trello_list(list_name: str) -> bool:
    """
    Archive a Trello list by its name.

    Args:
        list_name (str): The name of the Trello list to archive.

    Returns:
        bool: True if the list was archived successfully, False if the list does not exist.

    Raises:
        Exception: If the list cannot be archived due to an API error.
    """
    list_id = get_trello_list_id(list_name, include_archived=True)
    if list_id is None:
        # The list does not exist
        return False

    # Archive the list
    url = f"https://api.trello.com/1/lists/{list_id}/closed"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'value': 'true'
    }
    response = requests.put(url, params=query)

    if response.status_code == 200:
        return True
    else:
        raise Exception(f"Failed to archive the list '{list_name}': {response.status_code}, {response.text}")
    


    # Function to get a card ID by name and list name
def get_card_id(card_name: str, list_name: str) -> Optional[str]:
    """
    Get the ID of a card by its name and the name of the list it is in.

    Args:
        card_name (str): The name of the card.
        list_name (str): The name of the list containing the card.

    Returns:
        Optional[str]: The card ID if found, else None.
    """
    list_id = get_trello_list_id(list_name)
    if list_id is None:
        # The list does not exist
        return None

    # Get cards in the list
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    query_params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        cards = response.json()
        for card in cards:
            if card['name'].lower() == card_name.lower():
                return card['id']
        # Card not found
        return None
    else:
        raise Exception(f"Failed to fetch cards from Trello: {response.status_code}, {response.text}")

# Function to create a checklist in a card
def create_checklist_in_card(card_id: str, checklist_name: str) -> dict:
    """
    Create a checklist in a specified Trello card.

    Args:
        card_id (str): The ID of the Trello card.
        checklist_name (str): The name of the checklist to create.

    Returns:
        dict: The created checklist's details.

    Raises:
        Exception: If the checklist cannot be created due to an API error.
    """
    url = "https://api.trello.com/1/checklists"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idCard': card_id,
        'name': checklist_name
    }
    response = requests.post(url, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create checklist: {response.status_code}, {response.text}")

# Function to get a checklist ID by name and card ID
def get_checklist_id(card_id: str, checklist_name: str) -> Optional[str]:
    """
    Get the ID of a checklist by its name and the card ID it is in.

    Args:
        card_id (str): The ID of the card containing the checklist.
        checklist_name (str): The name of the checklist.

    Returns:
        Optional[str]: The checklist ID if found, else None.
    """
    url = f"https://api.trello.com/1/cards/{card_id}/checklists"
    query_params = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        checklists = response.json()
        for checklist in checklists:
            if checklist['name'].lower() == checklist_name.lower():
                return checklist['id']
        # Checklist not found
        return None
    else:
        raise Exception(f"Failed to fetch checklists from Trello: {response.status_code}, {response.text}")

# Function to add an item to a checklist
def add_item_to_checklist(checklist_id: str, item_name: str) -> dict:
    """
    Add an item to a specified Trello checklist.

    Args:
        checklist_id (str): The ID of the Trello checklist.
        item_name (str): The name of the item to add to the checklist.

    Returns:
        dict: The added checklist item's details.

    Raises:
        Exception: If the item cannot be added due to an API error.
    """
    url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'name': item_name,
        'checked': 'false'
    }
    response = requests.post(url, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add item to checklist: {response.status_code}, {response.text}")