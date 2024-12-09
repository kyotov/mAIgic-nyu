import unittest
from src.gmail.api import GmailAPI
from src.gmail.models import Email

class TestRealGmailAPI(unittest.TestCase):
    """testing gmail api using real gmail account"""
    def test_fetch_latest_email(self):
        gmail_api = GmailAPI()
        email = gmail_api.fetch_latest_email()

        self.assertIsNotNone(email, "No email was fetched. Check your API connection.")
        self.assertIsInstance(email, Email, "The returned object should be an instance of Email")
        self.assertTrue(hasattr(email, 'email_id'), "Email object should have an ID")
        self.assertTrue(hasattr(email, 'snippet'), "Email object should have a snippet")

if __name__ == '__main__':
    unittest.main()
