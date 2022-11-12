from emailsystem.emailer import EmailSystem


def email_lottery_run_msg(message: str):
    emailer = EmailSystem()
    emailer.send_email(
        subject="New York Lottery",
        message_html=f"""
            {message}
        """,
    )
    # TODO include ticket information
    # Format
    # Winning ticket - draw date -
    # tickets - color the matches - show the amount won
    #
