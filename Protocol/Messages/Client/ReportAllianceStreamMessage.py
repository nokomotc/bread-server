from ByteStream.Reader import Reader
from Protocol.Messages.Server.ReportUserStatusMessage import ReportUserStatusMessage
import requests, datetime, json

class ReportAllianceStreamMessage(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readLong()
        self.ReportedID = self.readLong()

    def process(self, db):
        reported_data = db.load_player_account_by_id(self.ReportedID)
        club_data = db.load_club(reported_data['ClubID']) 
        club_role = 0
        reported_club_role = 0 
        if self.player.club_role == 1:
            club_role = "Участник" 
        if self.player.club_role == 2:
            club_role = "Президент" 
        if self.player.club_role == 3:
            club_role = "Ветеран"
        if self.player.club_role == 4:
            club_role = "Вице-Президент"
        if reported_data['ClubRole'] == 1:
            reported_club_role = "Участник" 
        if reported_data['ClubRole'] == 2:
            reported_club_rolee = "Президент" 
        if reported_data['ClubRole'] == 3:
            reported_club_role = "Ветеран"
        if reported_data['ClubRole'] == 4:
            reported_club_role = "Вице-Президент"
        message_data = {
        'chat_id': "<removed by @CustomBrawlLeak>",
        'text': f"• *Новая жалоба*, @BreadTG!\n - Автор жалобы: {self.player.name}.\n - ID Автора жалобы: {self.player.ID}.\n - ID Клуба автора жалобы: {self.player.club_id}.\n - Роль автора жалобы: {club_role}.\n - Ник зарепорченного: {reported_data['Name']}.\n - Роль зарепорченного в клубе: {reported_club_role}.\n - Время жалобы: {str(datetime.datetime.now())}.\n",
        'parse_mode': 'Markdown',
        'reply_markup': json.dumps({'inline_keyboard':[[{"text":"Замутить на 1 день","callback_data":"mute_1d"}, {"text":"Забанить на 3 дня","callback_data":"ban_3d"}]]})
        }
        try:
            request = requests.post('https://api.telegram.org/bot<removed by @CustomBrawlLeak>/sendMessage', data=message_data)
            ReportUserStatusMessage(self.client, self.player, self.ReportedID).send()
        except:
            raise