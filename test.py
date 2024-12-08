import unittest
from gmail import GmailNotifier
import os
from dotenv import load_dotenv

class TestGmailNotifier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        load_dotenv()
        cls.credentials_file = os.getenv('GOOGLE_CLIENT_SECRET')
        cls.notifier = GmailNotifier(cls.credentials_file)

    def test_fetch_new_emails(self):
        sender, subject = self.notifier.fetch_new_emails()

        self.assertIsNotNone(sender, "Sender should not be None.")
        self.assertIsNotNone(subject, "Subject should not be None.")

        print(f"New email from: {sender}")
        print(f"Subject: {subject}")

if __name__ == "__main__":
    unittest.main()
