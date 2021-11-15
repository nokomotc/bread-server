from ByteStream.Reader import Reader
from Protocol.Messages.Server.AllianceResponseMessage import AllianceResponseMessage
from Protocol.Messages.Server.MyAllianceMessage import MyAllianceMessage
from Protocol.Messages.Server.AllianceStreamMessage import AllianceStreamMessage
import time

class JoinAllianceMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.club_id = self.readLong()

    def process(self, db):
        self.player.club_id = self.club_id
        self.player.club_role = 1

        club_data = db.load_club(self.club_id)
        if len(club_data['Members']) >= 100:
            AllianceResponseMessage(self.client, self.player, 42).send()
        else:
            club_data['Members'].append(
                {
                    f'Name': self.player.name,
                    'ID': self.player.ID,
                    'Role': self.player.club_role,
                    'Trophies': self.player.trophies,
                    'ProfileIcon': self.player.profile_icon,
                    'NameColor': self.player.name_color,
                    'Status': 2
                }
            )
            self.player.message_tick = club_data['Messages'][-1]['Tick'] if club_data['Messages'] else self.player.message_tick
            self.player.message_tick += 1
            message = {'Event': 4, 'Message': 3, 'PlayerID': self.player.ID, 'PlayerName': self.player.name, 'PlayerRole': self.player.club_role, 'Tick': self.player.message_tick, 'Time': time.time()}
            club_data['Messages'].append(message)
            for members in club_data['Members']:
                AllianceStreamMessage(self.client, self.player, club_data['Messages']).sendByID(members[str('ID')])
                AllianceStreamMessage(self.client, self.player, club_data['Messages']).send()
            db.update_club(self.club_id, 'Messages', club_data['Messages'])
            db.update_club(self.club_id, 'Members', club_data['Members'])
            db.update_club(self.club_id, 'Trophies', club_data['Trophies'] + self.player.trophies)
            db.update_player_account(self.player.token, 'ClubID', self.player.club_id)
            db.update_player_account(self.player.token, 'ClubRole', self.player.club_role)

            AllianceResponseMessage(self.client, self.player, 40).send()
            MyAllianceMessage(self.client, self.player, club_data).send()
            AllianceStreamMessage(self.client, self.player, club_data['Messages']).send()
