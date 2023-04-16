class DecryptedMessage:
    def __init__(self, author_id, datetime):
        self.author_id = author_id
        self.datetime = datetime


class DecryptedTextMessage(DecryptedMessage):
    def __init__(self, author_id, text, datetime):
        super().__init__(author_id, datetime)
        self.text = text


class DecryptedFileMessage(DecryptedMessage):
    def __init__(self, author_id, file, filename, datetime):
        super().__init__(author_id, datetime)
        self.file = file
        self.filename = filename

