import json
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
            try:
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
                    Always respond with correct JSON format. 
                    Do not include anything outside the JSON.
                    Do not include any null fields in the result.

                    Please analyze the following email and summarize as follows:
                    
                    * spam: ... (a % probability that the email is spam)
                    * urgent: ... (a % probability that the email is urgent)
                    * important: ... (a % probability that the email is important)
                    * action_needed: ... (a % probability that the email requires action)                
                    * category: ...
                    * suggested_action: ...

                    In case the email is a shipping notification, also include:
                    * sender: ...
                    * tracking_number: ...
                    * tracking_url: ...
                    * expected_on: ... (delivery date)
                    * package_content: ... 

                    * snippet: ... (snippet summary of the body of the email)

                    (do not include any null fields in the result)
                    """
                )

                print(header)

                response = thread.post(email)
                print(f"mAIgic: {response}")

                j = json.loads(response)
                j["__from"] = m.from_
                j["__subject"] = m.subject
                j["__date"] = m.date
                j["__id"] = m.id

                f.write(f"{json.dumps(j, indent=2)},\n")
                f.flush()
            except Exception as e:
                print(f"Error: {e}")

            # if i > 3:
            #     break


def nano() -> None:
    import sys

    # NOTE: there must be a better way for this...
    repo_root = __file__.split(f"{__name__}/src")[0]
    sys.path.append(f"{repo_root}/build/ky_cc_calculator")

    from _calculator import KyCalculator

    c = KyCalculator(42)
    print(c.add(1, 2))


def main() -> None:
    nano()
    # main_mix()


if __name__ == "__main__":
    main()
