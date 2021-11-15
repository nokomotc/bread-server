from Utils.Helpers import Helpers
from ByteStream.Reader import Reader
from Protocol.Messages.Server.AllianceResponseMessage import AllianceResponseMessage
from Protocol.Messages.Server.MyAllianceMessage import MyAllianceMessage
from Protocol.Messages.Server.AllianceDataMessage import AllianceDataMessage
import time
from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage

class KickAllianceMemberMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.MemberID = self.readLong()

    def process(self, db):
        target = db.load_player_account_by_id(self.MemberID)
        club_data = db.load_club(self.player.club_id)
        
        for member in club_data['Members']:
            if member['ID'] == self.MemberID:
                del club_data['Members'][club_data['Members'].index(member)]
                db.update_club(self.player.club_id, 'Members', club_data['Members'] )
                db.update_player_account_by_id(member['ID'], 'ClubID', 0) 
                db.update_player_account(member['ID'], 'ClubRole', 0)

        self.player.message_tick = club_data['Messages'][-1]['Tick'] if club_data['Messages'] else self.player.message_tick
        self.player.message_tick += 1
        message = {'Event': 4, 'Message': 1, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'TargetName': target['Name'], 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
        club_data['Messages'].append(message)
        for members in club_data['Members']:
            AllianceStreamMessage(self.client, self.player, club_data['Messages']).sendByID(members[str('ID')])
            AllianceStreamMessage(self.client, self.player, club_data['Messages']).send()
        db.update_club(self.player.club_id, 'Trophies', club_data['Trophies'] - member['Trophies'])
        db.update_club(self.player.club_id, 'Messages', club_data['Messages'])
        AllianceResponseMessage(self.client, self.player, 70).send()
        AllianceResponseMessage(self.client, self.player, 100).sendByID(self.MemberID)
        AllianceDataMessage(self.client, self.player, club_data).send()
        MyAllianceMessage(self.client, self.player, {'ID':0}).sendByID(self.MemberID)  
