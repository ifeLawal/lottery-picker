from emailsystem.emailer import EmailSystem


def email_ticket_results():
    emailer = EmailSystem()
    emailer.send_via_gmail(
        "ifelaw2439@gmail.com",
        """
    
                           """,
    )
    # TODO include ticket information
    # Format
    # Winning ticket - draw date -
    # tickets - color the matches - show the amount won
    #
