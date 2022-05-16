from typing import List
class Emailer():
    '''
    The email module. Does not actually email anyone
    but prints the hypothetical action to console.
    '''

    def __init__(self, email: str) -> None:
        self.email = email

    def send(self, event_name: str, email: str) -> None:
        print(f"Email invite for {event_name} event sent to recipient(s): {email}.")

    def notify(self, email: str, msg: str) -> None:
        print(f"Email with message: \n-----\n{msg}\n-----\nsent to recipient(s): {email}.")

    def add_event(self, event_name: str, emails: List[str]) -> None:
        self.send(event_name, emails)

    def update_event(self, event_name: str, emails: List[str]) -> None:
        self.notify(emails, f"Event {event_name} updated.")

    def remove_event(self, event_name: str, emails: List[str]) -> None:
        self.notify(emails, f"Event {event_name} deleted.")
