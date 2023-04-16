class DecryptedMessage:
    def __init__(self, author_id, datetime, cipher_mode):
        self.author_id = author_id
        self.datetime = datetime
        self.cipher_mode = cipher_mode


class DecryptedTextMessage(DecryptedMessage):
    def __init__(self, author_id, text, datetime, cipher_mode):
        super().__init__(author_id, datetime, cipher_mode)
        self.text = text


class DecryptedFileMessage(DecryptedMessage):
    def __init__(self, author_id, file, filename, datetime, cipher_mode):
        super().__init__(author_id, datetime, cipher_mode)
        self.file = file
        self.filename = filename

