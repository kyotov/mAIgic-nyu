from src.gmail.api import GmailAPI

def main():
    """basic main function to see the working of the api"""
    try:
        gmail_api = GmailAPI()
        latest_email = gmail_api.fetch_latest_email()

        if latest_email:
            print("Latest Email:")
            print(f"ID: {latest_email.email_id}")
            print(f"From: {latest_email.sender}")
            print(f"Subject: {latest_email.subject}")
            print(f"Snippet: {latest_email.snippet}")
        else:
            print("No new emails found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
