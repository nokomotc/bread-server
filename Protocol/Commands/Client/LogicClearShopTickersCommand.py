from ByteStream.Reader import Reader
from Files.CsvLogic.Cards import Cards
from Files.CsvLogic.Characters import Characters

class LogicClearShopTickersCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readVInt()
        self.readVInt() 
        self.readLogicLong()
        print(self.readVInt()  ) 
        print(self.readVInt()  )      


    def process(self, db):
        pass