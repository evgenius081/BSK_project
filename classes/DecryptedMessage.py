from enum import Enum


class Status(Enum):
    Sending = "Sending"
    Sent = "Sent"
    Read = "Read"


class DecryptedMessage:
    def __init__(self, author_id, datetime, status):
        self.author_id = author_id
        self.datetime = datetime
        self.status = status


class DecryptedTextMessage(DecryptedMessage):
    def __init__(self, author_id, text, datetime, status):
        super().__init__(author_id, datetime, status)
        self.text = text


class DecryptedFileMessage(DecryptedMessage):
    def __init__(self, author_id, file, filename, datetime, status):
        super().__init__(author_id, datetime, status)
        self.file = file
        self.filename = filename

