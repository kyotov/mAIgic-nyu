# test_slack.py
import unittest
from unittest.mock import MagicMock, patch

class TestSlackBot(unittest.TestCase):
    def test_message_hello(self):
        with patch('slack_bolt.App') as MockApp:
            # Create a mock instance of App
            mock_app_instance = MockApp.return_value

            # Define a decorator function to capture the handler
            def message_decorator(*args, **kwargs):
                def wrapper(func):
                    # Capture the handler function
                    self.handler_function = func
                return wrapper

            mock_app_instance.message.side_effect = message_decorator

            # Import Slack app
            import src.maigic_nyu.slack.slack

            say = MagicMock()
            message = {
                'user': 'U123456',
                'text': 'Hello, bot!'
            }

            # Call the handler function with the mock 'say' and 'message'
            self.handler_function(message=message, say=say)

            expected_response = "Hey there <@U123456>! I am responding to: Hello, bot!"
            say.assert_called_once_with(expected_response)

if __name__ == '__main__':
    unittest.main()
