from ByteStream.Writer import Writer
import time

class AllianceStreamMessage(Writer):

    def __init__(self, client, player, msg):
        super().__init__(client)
        self.id = 24311
        self.player = player
        self.msg = msg


    def encode(self):
        if self.player.club_id != 0:
            self.writeVInt(min(len(self.msg), 30))
            for x in self.msg[-30:]:
                self.writeVInt(x['Event'])
                self.writeVInt(0)
                self.writeVInt(x['Tick'])
                self.writeLogicLong(x['PlayerID'])
                self.writeString(x['PlayerName'])
                self.writeVInt(x['PlayerRole'])
                self.writeVInt(int(time.time() - x['Time']))
                self.writeVInt(0)

                if x['Event'] == 4:
                    self.writeVInt(x['Message'])
                    self.writeVInt(1)
                    self.writeLogicLong(x['PlayerID'])
                    if x['Message'] in [1, 2, 5, 6]:
                        self.writeString(x['TargetName']) # <Мистери> повышается в звании игроком <sender>. Поздравляем!
                    else:
                        self.writeString(x['PlayerName'])

                else:
                    self.writeString(x['Message'])
        else:
            self.writeVInt(0)

