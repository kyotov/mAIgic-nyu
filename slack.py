from slack_sdk import WebClient


def main():
    client = WebClient(
        token="<token>"
    )

    # r = client.users_list()
    # r.validate()
    # pprint(r.data)

    # r = client.conversations_open(channel="U01C91V6QNQ")
    # r.validate()

    r = client.chat_postMessage(channel="C01CAH729TK", text="hello!")
    r.validate()


if __name__ == "__main__":
    main()
