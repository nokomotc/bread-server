from ByteStream.Reader import Reader
from Protocol.Messages.Server.AllianceResponseMessage import AllianceResponseMessage
from Protocol.Messages.Server.MyAllianceMessage import MyAllianceMessage
from Protocol.Messages.Server.AllianceDataMessage import AllianceDataMessage
from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage
import time


class LeaveAllianceMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        pass

    def process(self, db):
        club_data = db.load_club(self.player.club_id)

        if len(club_data['Members']) == 1:
            db.delete_club(self.player.club_id)
        else:
            for member in club_data['Members']:
                if member['ID'] == self.player.ID:
                    del club_data['Members'][club_data['Members'].index(member)]
                    if self.player.club_role == 2:
                        temprole = list(sorted(club_data['Members'], key=lambda _: _['Role']))[-1]['Role']
                        temp = list(filter(lambda _: _['Role'] == temprole, club_data['Members']))
                        temp = list(sorted(temp, key=lambda _: _['Trophies']))[-1]
                        db.update_player_account_by_id(temp['ID'], 'ClubRole', 2)
                        temp['Role'] = 2
                        db.update_club(self.player.club_id, 'Members', club_data['Members'] )
                    else:
                        pass
                        db.update_club(self.player.club_id, 'Members', club_data['Members'] )    

        AllianceDataMessage(self.client, self.player, club_data).sendByID(club_data['Members']) 
        db.update_player_account(self.player.token, 'ClubID', 0)
        self.player.message_tick = club_data['Messages'][-1]['Tick'] if club_data['Messages'] else self.player.message_tick
        self.player.message_tick += 1
        message = {'Event': 4, 'Message': 4, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
        club_data['Messages'].append(message)
        for members in club_data['Members']:
            AllianceStreamMessage(self.client, self.player, club_data['Messages']).sendByID(members[str('ID')])
            AllianceStreamMessage(self.client, self.player, club_data['Messages']).send()
            
        db.update_club(self.player.club_id, 'Messages', club_data['Messages'])
        db.update_club(self.player.club_id, 'Trophies', club_data['Trophies'] - self.player.trophies)
        AllianceResponseMessage(self.client, self.player, 80).send()
        MyAllianceMessage(self.client, self.player, {'ID':0}).send()