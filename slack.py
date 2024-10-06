from slack_sdk import WebClient
import os


def main():
    client = WebClient(
        token=os.getenv("SLACK_BOT_TOKEN")
    )

    # r = client.users_list()
    # r.validate()
    # pprint(r.data)

    # r = client.conversations_open(channel="U01C91V6QNQ")
    # r.validate()

    r = client.chat_postMessage(channel=os.getenv("SLACK_CHANNEL_ID"),
                                text="hello!")
    r.validate()


if __name__ == "__main__":
    main()
