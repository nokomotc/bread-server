from ByteStream.Writer import Writer

class ReportUserStatusMessage(Writer):

    def __init__(self, client, player, ReportedID):
        super().__init__(client)
        self.id = 20117
        self.player = player
        self.ReportedID = ReportedID

    def encode(self):
        self.writeInt(1)
        self.writeInt(self.ReportedID)