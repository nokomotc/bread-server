from ByteStream.Reader import Reader
from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage
import time
class ChatToAllianceStreamMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.msg = self.readString()

    def process(self, db):
        self.commandslist = ['/unlock']
        if self.msg == '/unlock':
            for x in self.player.brawlers_id:
                self.player.brawlers_level[str(x)] = 8
                self.player.brawlers_powerpoints[str(x)] = 1410
                db.update_player_account(self.player.token, 'UnlockedBrawlers', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46])
                db.update_player_account(self.player.token, 'BrawlersLevel', self.player.brawlers_level)
                db.update_player_account(self.player.token, 'BrawlersPowerPoints', self.player.brawlers_powerpoints)
        club_data = db.load_club(self.player.club_id)

        self.player.message_tick = club_data['Messages'][-1]['Tick'] if club_data['Messages'] else self.player.message_tick
        self.player.message_tick += 1

        message = {'Event': 2 ,'Message': self.msg, 'PlayerID': self.player.ID, 'PlayerName':self.player.name, 'PlayerRole':self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
        if self.msg not in self.commandslist:
            club_data['Messages'].append(message)
            db.update_club(self.player.club_id, 'Messages', club_data['Messages'])

            for member in club_data['Members']:
                member_id = member['ID']
                AllianceStreamMessage(self.client, self.player, [message]).sendByID(member_id)