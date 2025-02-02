import textwrap
import ky_mail_api
import ky_mail_gmail_impl as _  # noqa: F401


def main() -> None:
    c = ky_mail_api.get_client()

    for i, m in enumerate(c.get_messages()):
        print(
            textwrap.dedent(f"""
                --------------------------------------------------------------------------------
                --------------------------------------------------------------------------------
                From: {m.from_}
                Subject: {m.subject}
                Date: {m.date}
                URL: https://mail.google.com/mail/u/0/#all/{m.id}
                --------------------------------------------------------------------------------
                """)
        )
        print(m.body)

        if i > 10:
            break


if __name__ == "__main__":
    main()
