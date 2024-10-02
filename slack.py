from slack_sdk import WebClient


def main():
    client = WebClient(
        token="xoxb-1402866809893-7831129119424-vgQR7hEp45Iic0qCwen5qLQZ"
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
