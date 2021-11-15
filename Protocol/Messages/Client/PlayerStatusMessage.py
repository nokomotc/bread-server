from Protocol.Messages.Server.TeamMessage import TeamMessage
from Protocol.Messages.Server.AllianceDataMessage import AllianceDataMessage
from ByteStream.Reader import Reader
from Utils.Helpers import Helpers
import time

class PlayerStatusMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client


    def decode(self):
        self.player.status = self.readVInt() # Player State | 11: Events, 10: Brawlers, 9: Writing..., 8: Training, 7: Spectactor, 6: Offline, 5: End Combat Screen, 4: Searching, 3: Not Ready, 2: AFK, 1: In Combat, 0: OffLine

    def process(self, db):
        if self.player.club_id != 0:
            club_data = db.load_club(self.player.club_id)
            for member in club_data['Members']:
                if member['ID'] == self.player.ID:
                    if self.player.status != -64:
                        member['Status'] = self.player.status
                    db.update_club(self.player.club_id, 'Members', club_data['Members'])
                AllianceDataMessage(self.client, self.player, club_data).sendByID(member['ID'])
        else:
            pass            