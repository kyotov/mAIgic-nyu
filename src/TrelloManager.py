"""TrelloManager module interacts with the Trello API to create cards."""
import logging
import os

import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HTTP_OK = 200

class TrelloManager:

    """A class to interact with the Trello API.

    This class provides methods to retrieve and manipulate data on Trello boards,
    such as creating lists, retrieving board and list details, and creating cards.

    Attributes:
        api_key (str): The API key for authenticating with Trello.
        token (str): The OAuth token for accessing Trello API.
        BASE_URL (str): The base URL for Trello API requests.

    """

    def __init__(self) -> None:
        """Initialize TrelloManager with API credentials.

        This method loads the API key and OAuth token from environment variables using
        the `dotenv` package. These credentials are necessary for interacting with the
        Trello API.

        """
        # Retrieve API key and token from environment variables
        load_dotenv()
        self.api_key = os.getenv("TRELLO_API_KEY")
        self.token = os.getenv("TRELLO_OAUTH_TOKEN")
        self.BASE_URL = "https://api.trello.com/1"

    def get_full_board_info(self, short_board_id: str) -> str:
        """Get full board information from Trello.

        Args:
            short_board_id (str): The short ID of the Trello board.

        Returns:
            str: The full board ID.

        """
        url = f"{self.BASE_URL}/boards/{short_board_id}"
        query = {
            "key": self.api_key,
            "token": self.token,
        }
        response = requests.get(url, params=query, timeout=10)

        if response.status_code == HTTP_OK:
            board_info = response.json()
            return board_info["id"]
        return ""

    def get_lists(self, board_id: str) -> list:
        """Get all lists in the specified Trello board.

        Args:
            board_id (str): The full ID of the Trello board.

        Returns:
            list: A list of list IDs.

        """
        url = f"{self.BASE_URL}/boards/{board_id}/lists"
        query = {
            "key": self.api_key,
            "token": self.token,
        }
        response = requests.get(url, params=query, timeout=10)

        list_id = []
        if response.status_code == HTTP_OK:
            lists = response.json()
            list_id = [lst["id"] for lst in lists]

        return list_id

    def create_card(self, list_id: str, name: str, desc: str) -> None:
        """Create a new card in the specified list.

        Args:
            list_id (str): The ID of the list where the card will be created.
            name (str): The name of the card.
            desc (str): The description of the card (optional).

        """
        url = f"{self.BASE_URL}/cards"
        query = {
            "key": self.api_key,
            "token": self.token,
            "idList": list_id,
            "name": name,
            "desc": desc,
        }
        response = requests.post(url, params=query, timeout=10)

        if response.status_code == HTTP_OK:
            logger.info("Card successfully created!")

    def get_list_name(self, list_id: str) -> str:
        """Get the list name of a specific list id in the specific board.

        Args:
            list_id (str): the id of the specific list.

        Returns:
            str: the name of the specific list.

        """
        url = f"{self.BASE_URL}/lists/{list_id}"
        query = {
            "key": self.api_key,
            "token": self.token,
        }
        response = requests.get(url, params=query, timeout=10)

        if response.status_code == HTTP_OK:
            list_info = response.json()
            return list_info.get("name", "No name found")

        return ""

    def create_a_list(self, list_name: str, id_board: str) -> str:
        """Create a new list on the specified Trello board.

        Args:
            list_name (str): The name of the new list.
            id_board (str): The ID of the board where the list will be created.

        Returns:
            str: The ID of the created list, or an empty string if creation failed.

        """
        url = f"{self.BASE_URL}/lists"
        query = {
            "idBoard": id_board,
            "name": list_name,
            "key": self.api_key,
            "token": self.token,
        }

        response = requests.post(url, params=query, timeout=10)
        if response.status_code == HTTP_OK:
            logger.info("List creation succeed!")
            return response.json().get("id")

        logger.info("List creation failed")
        return ""

if __name__ == "__main__":
    # go to your target workspace and board, you will see a short id in your url
    # example: https://trello.com/b/{short_board_id}/{board_name}
    trello = TrelloManager()
    short_board_id = "your_board_id"
    full_board_id = trello.get_full_board_info(short_board_id)

    if full_board_id:
        list_ids = trello.get_lists(full_board_id)
        target_id = ""

        for list_id in list_ids:
            if trello.get_list_name(list_id) == "Important":
                target_id = list_id
                break
        if not target_id:
            list_name = "Important"
            target_id = trello.create_a_list(list_name, full_board_id)

        trello.create_card(target_id, "task_name", "An important thing to do")



