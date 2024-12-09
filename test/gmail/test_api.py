import unittest
from unittest.mock import patch, MagicMock
from src.gmail.api import GmailAPI
from src.gmail.models import Email

class TestGmailAPI(unittest.TestCase):
    """testing gmail api"""
    @patch('src.gmail.api.build')
    @patch('src.gmail.api.get_credentials')
    def test_fetch_latest_email(self, mock_get_credentials, mock_build):
        service_mock = MagicMock()
        mock_build.return_value = service_mock
        service_mock.users().messages().list().execute.return_value = {
            'messages': [{'id': '123'}]
        }
        service_mock.users().messages().get().execute.return_value = {
            'id': '123',
            'snippet': 'Test snippet',
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'Subject', 'value': 'Test Subject'}
                ]
            }
        }

        gmail_api = GmailAPI()
        email = gmail_api.fetch_latest_email()

        self.assertIsNotNone(email, "Email should not be None")
        self.assertIsInstance(email, Email, "The returned object should be an instance of Email")
        self.assertEqual(email.email_id, '123', "Email ID should match the mocked response")
        self.assertEqual(email.sender, 'sender@example.com', "Email sender should match the mocked response")
        self.assertEqual(email.subject, 'Test Subject', "Email subject should match the mocked response")
        self.assertEqual(email.snippet, 'Test snippet', "Email snippet should match the mocked response")

if __name__ == '__main__':
    unittest.main()
