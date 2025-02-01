import ky_mail_gmail_impl as _  # noqa: F401

import ky_mail_api


def main() -> None:
    c = ky_mail_api.get_client()

    for i, m in enumerate(c.get_messages()):
        print(i, m.get_body())


if __name__ == "__main__":
    main()
