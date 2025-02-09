Collaboration doc for this initiative: https://docs.google.com/document/d/1duhM5Ufkq_doBnMvHo65S7cplmUJw4KqQvDRfZlmj7s/edit

To get started, you can follow the below steps:
1. Clone the kyotov/maigic repository.
2. Checkout desired brach.
3. uv sync
5. cd ky_test 
7. uv build
8. Replace credentials.json with your credentials file. See related note below.
8. uv run main


Note that you may need to do the following steps to get the credentials.json file.
1. Enable Gmail API
2. Go to the Google Cloud Console.
3. Create a new project or select an existing one.
4. Navigate to "APIs & Services" > "Library" and enable the Gmail API.
5. Go to "APIs & Services" > "Credentials" and click "Create Credentials."
6. Choose "OAuth Client ID" and follow the setup instructions.
7. Download the JSON credentials file.