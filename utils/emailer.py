
class Emailer():

    def __init__(self, email: str) -> None:
        self.email = email

    def send(self) -> None:
        print(f"Email notification for this event sent to {self.email}.")