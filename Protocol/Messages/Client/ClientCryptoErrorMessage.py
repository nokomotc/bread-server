from ByteStream.Reader import Reader
from Utils.Helpers import Helpers
from Protocol.Messages.Server.LoginFailedMessage import LoginFailedMessage

class ClientCryptoErrorMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        pass

    def process(self, db):
        pass

