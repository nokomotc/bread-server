from ByteStream.Reader import Reader
from Utils.Helpers import Helpers
from Logic.Home.LogicShopData import LogicShopData
from Protocol.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage

class LogicClaimRankUpRewardCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        print(self.readVInt())
        self.box_id = self.readDataReference()
        print(self.readVInt())
        self.ispaidpass = self.readVInt() # 9 = Premium Pass, 10 = Free Pass

    def process(self, db):
        self.player.delivery_items = {'Count': 1, 'Type': Helpers.get_box_type(self, 1)}

        self.player.db = db
        AvailableServerCommandMessage(self.client, self.player, 203, {}).send()



