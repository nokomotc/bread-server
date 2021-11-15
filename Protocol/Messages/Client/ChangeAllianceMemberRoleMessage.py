from Utils.Helpers import Helpers
from ByteStream.Reader import Reader
from Protocol.Messages.Server.AllianceResponseMessage import AllianceResponseMessage
from Protocol.Messages.Server.AllianceDataMessage import AllianceDataMessage
import time
from Protocol.Messages.Server.MyAllianceMessage import MyAllianceMessage
from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage
class ChangeAllianceMemberRoleMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.TargetID = self.readLong()
        self.TargetedRole = self.readVInt()
        
    def process(self, db):
        club_data = db.load_club(self.player.club_id)
        target = db.load_player_account_by_id(self.TargetID)
        self.player.message_tick = club_data['Messages'][-1]['Tick'] if club_data['Messages'] else self.player.message_tick
        self.player.message_tick += 1

        for member in club_data['Members']:
            if member['ID'] == self.TargetID:
                if member['Role'] == 1 and self.TargetedRole == 3:
                    AllianceResponseMessage(self.client, self.player, 81).send()
                    MyAllianceMessage(self.client, self.player, club_data).sendByID(self.TargetID)  
                    AllianceResponseMessage(self.client, self.player, 101).sendByID(self.TargetID)
                    message = {'Event': 4, 'Message': 5, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'TargetName': target['Name'], 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
                if member['Role'] == 3 and self.TargetedRole == 4:
                    MyAllianceMessage(self.client, self.player, club_data).sendByID(self.TargetID)
                    AllianceResponseMessage(self.client, self.player, 81).send()
                    AllianceResponseMessage(self.client, self.player, 101).sendByID(self.TargetID)
                    message = {'Event': 4, 'Message': 5, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'TargetName': target['Name'], 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
                #if member['Role'] == 4 and self.TargetedRole == 2:
                 #   AllianceResponseMessage(self.client, self.player, 82).send()
                 #   AllianceResponseMessage(self.client, self.player, 102).sendByID(self.TargetID)
                    db.update_club(self.player.club_id, 'Members', club_data['Members'] )
                if member['Role'] == 4 and self.TargetedRole in [3, 1]:
                    MyAllianceMessage(self.client, self.player, club_data).sendByID(self.TargetID)
                    AllianceResponseMessage(self.client, self.player, 82).send()
                    AllianceResponseMessage(self.client, self.player, 102).sendByID(self.TargetID)
                    message = {'Event': 4, 'Message': 6, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'TargetName': target['Name'], 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
                if member['Role'] in [2, 3, 4] and self.TargetedRole in [3, 1]:
                    MyAllianceMessage(self.client, self.player, club_data).sendByID(self.TargetID)
                    AllianceResponseMessage(self.client, self.player, 82).send()
                    AllianceResponseMessage(self.client, self.player, 102).sendByID(self.TargetID)
                    message = {'Event': 4, 'Message': 6, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'TargetName': target['Name'], 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
                if self.player.club_role == 2 and self.TargetedRole == 2:
                    for member in club_data['Members']:
                        if member['ID'] == self.player.ID:
                            member['Role'] = 4
                        db.update_player_account_by_id(self.player.ID, 'ClubRole', 4) 
                    MyAllianceMessage(self.client, self.player, club_data).sendByID(self.TargetID)
                    AllianceResponseMessage(self.client, self.player, 81).send()
                    AllianceResponseMessage(self.client, self.player, 101).sendByID(self.TargetID)
                    message = {'Event': 4, 'Message': 5, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'TargetName': target['Name'], 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()} 
                    message = {'Event': 4, 'Message': 5, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'TargetName': target['Name'], 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
                member['Role'] = self.TargetedRole

                db.update_club(self.player.club_id, 'Members', club_data['Members'] )
        club_data['Messages'].append(message)
        db.update_club(self.player.club_id, 'Messages', club_data['Messages'] )
        for members in club_data['Members']:
            AllianceStreamMessage(self.client, self.player, club_data['Messages']).sendByID(members[str('ID')])
            AllianceStreamMessage(self.client, self.player, club_data['Messages']).send()
        db.update_player_account_by_id(self.TargetID, 'ClubRole', self.TargetedRole)                
        AllianceDataMessage(self.client, self.player, club_data).send()
        AllianceDataMessage(self.client, self.player, club_data).sendByID(member['ID']) 
