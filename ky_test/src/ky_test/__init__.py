import logging
import textwrap

import ky_ai_assistant_api
import ky_ai_assistant_openai  # noqa: F401
import ky_mail_api
import ky_mail_gmail_impl  # noqa: F401

logging.basicConfig(level=logging.WARNING)

# logging.getLogger(ky_ai_assistant_openai._impl.__name__).setLevel(logging.DEBUG)


def main_gmail() -> None:
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


def main_ai_assistant() -> None:
    c = ky_ai_assistant_api.get_client()
    t = c.new_thread("Hello, how are you?")
    print(t.post("I'm good, how are you?"))
    print(t.post("I'm good too!"))


def main_mix() -> None:
    c = ky_mail_api.get_client()
    a = ky_ai_assistant_api.get_client()

    with open("email.log", "w") as f:
        for i, m in enumerate(c.get_messages()):
            header = textwrap.dedent(f"""
                    --------------------------------------------------------------------------------
                    --------------------------------------------------------------------------------
                    From: {m.from_}
                    Subject: {m.subject}
                    Date: {m.date}
                    URL: https://mail.google.com/mail/u/0/#all/{m.id}
                    --------------------------------------------------------------------------------
                    """)
            email = header + m.body

            thread = a.new_thread(
                """
                Please analyze the following email and summarize as follows (in json format):
                
                * spam: ... (a % probability that the email is spam)
                * urgent: ... (a % probability that the email is urgent)
                * category: ...
                * suggested action: ...

                In case the email is a shipping notification, also include:
                * sender: ...
                * tracking number: ...
                * tracking url: ...
                * expected on: ... (delivery date)
                * package content: ... 

                * snippet: ... (snippet summary of the body of the email)

                (do not include any null fields in the result)
                """
            )

            print(header)

            response = thread.post(email)
            print(f"mAIgic: {response}")

            f.write(f"{header}\n{response}\n\n")
            f.flush()

            # if i > 1:
            #     break


def main() -> None:
    main_mix()


if __name__ == "__main__":
    main()
