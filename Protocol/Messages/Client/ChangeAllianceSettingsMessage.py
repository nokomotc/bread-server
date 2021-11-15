from ByteStream.Reader import Reader
from Protocol.Messages.Server.AllianceResponseMessage import AllianceResponseMessage
from Protocol.Messages.Server.MyAllianceMessage import MyAllianceMessage
from Protocol.Messages.Server.AllianceDataMessage import AllianceDataMessage


class ChangeAllianceSettingsMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.club_id              = self.player.club_id
        self.club_desc            = self.readString()
        self.club_badge           = self.readDataReference()[1]
        self.club_region          = self.readDataReference()[1]
        self.club_type            = self.readVInt()
        self.club_req_trophies    = self.readVInt()
        self.club_family_friendly = self.readVInt()

    def process(self, db):
        club_data = db.load_club(self.club_id)
        if self.club_desc != club_data['Description']:
            db.update_club(self.club_id, 'Description', self.club_desc)

        if self.club_type != club_data['Type']:    
            db.update_club(self.club_id, 'Type', self.club_type)

        if self.club_badge != club_data['BadgeID']:    
            db.update_club(self.club_id, 'BadgeID', self.club_badge)

        if self.club_req_trophies != club_data['RequiredTrophies']:               
            db.update_club(self.club_id, 'RequiredTrophies', self.club_req_trophies)

        if self.club_family_friendly != club_data['FamilyFriendly']:               
            db.update_club(self.club_id, 'FamilyFriendly', self.club_family_friendly)

        club_data = db.load_club(self.club_id)
        for member in club_data['Members']:
            MyAllianceMessage(self.client, self.player, club_data).sendByID(member['ID'])
            AllianceDataMessage(self.client, self.player, club_data).sendByID(member['ID'])
        AllianceResponseMessage(self.client, self.player, 10).send()