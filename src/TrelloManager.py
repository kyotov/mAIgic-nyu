"""TrelloManager module interacts with the Trello API to create cards."""
import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()
# Retrieve API key and token from environment variables
api_key = os.getenv("TRELLO_API_KEY")
token = os.getenv("TRELLO_OAUTH_TOKEN")

BASE_URL = "https://api.trello.com/1"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HTTP_OK = 200
def get_full_board_info(short_board_id: str) -> str:
    """Get full board information from Trello.

    Args:
        short_board_id (str): The short ID of the Trello board.

    Returns:
        str: The full board ID.

    """
    url = f"{BASE_URL}/boards/{short_board_id}"
    query = {
        "key": api_key,
        "token": token,
    }
    response = requests.get(url, params=query, timeout=10)

    if response.status_code == HTTP_OK:
        board_info = response.json()
        return board_info["id"]
    return ""

def get_lists(board_id: str) -> list:
    """Get all lists in the specified Trello board.

    Args:
        board_id (str): The full ID of the Trello board.

    Returns:
        list: A list of list IDs.

    """
    url = f"{BASE_URL}/boards/{board_id}/lists"
    query = {
        "key": api_key,
        "token": token,
    }
    response = requests.get(url, params=query, timeout=10)

    list_id = []
    if response.status_code == HTTP_OK:
        lists = response.json()
        list_id = [lst["id"] for lst in lists]

    return list_id

def create_card(list_id: str, name: str, desc: str) -> None:
    """Create a new card in the specified list.

    Args:
        list_id (str): The ID of the list where the card will be created.
        name (str): The name of the card.
        desc (str): The description of the card (optional).

    """
    url = f"{BASE_URL}/cards"
    query = {
        "key": api_key,
        "token": token,
        "idList": list_id,
        "name": name,
        "desc": desc,
    }
    response = requests.post(url, params=query, timeout=10)

    if response.status_code == HTTP_OK:
        logger.info("Successfully created!")


if __name__ == "__main__":
    # go to your target workspace and board, you will see a short id in your url
    # example: https://trello.com/b/{short_board_id}/{board_name}
    short_board_id = "your_short_board_id"
    full_board_id = get_full_board_info(short_board_id)
    # to simply test, I just chose the first list to add a new card
    if full_board_id:
        list_ids = get_lists(full_board_id)
        if list_ids:
            create_card(list_ids[0], "new to-do",
                        "This is a new task created by the bot")