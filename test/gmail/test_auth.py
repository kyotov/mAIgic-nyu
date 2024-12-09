import unittest
from unittest.mock import patch, MagicMock
from src.gmail.auth import get_credentials

class TestAuthManager(unittest.TestCase):
    """testing auth manager"""
    @patch('src.gmail.auth.Credentials.from_authorized_user_file')
    @patch('src.gmail.auth.InstalledAppFlow')
    @patch('os.path.exists')
    def test_get_credentials(self, mock_exists, mock_flow, mock_from_file):
        mock_exists.return_value = True
        creds_instance = MagicMock()
        mock_from_file.return_value = creds_instance

        creds = get_credentials()

        self.assertIsNotNone(creds, "Credentials should not be None")
        mock_from_file.assert_called_once()  
        mock_flow.assert_not_called()  

if __name__ == '__main__':
    unittest.main()
