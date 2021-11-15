from ByteStream.Writer import Writer
from Utils.Helpers import Helpers

class TeamMessage(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 24124
        self.player = player

    def encode(self):
        self.writeVInt(1) # Тип комнаты
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeLong(1) # ID Комнаты

        self.writeVInt(1594036200)
        self.writeUInt8(0)
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeDataReference(15, self.player.map_id) # ID Карты

        self.writeVInt(1) # Счетчик игроков

        self.writeUInt8(1) # Владелец комнаты или нет

        self.writeLong(self.player.ID) # ID игрока

        self.writeDataReference(16, self.player.home_brawler) # Бравлер
        self.writeDataReference(29, self.player.home_skin) # Скин

        self.writeVInt(99999) # Кубки бравлера
        self.writeVInt(99999) # Высшие кубки бравлера
        self.writeVInt(10) # Уровень силы

        self.writeVInt(3) # Статус игрока
        self.writeUInt8(0) # Игрок готов или нет
        self.writeVInt(0) # Команда | 0 = Синий, 1 = Красный
        self.writeVInt(0)
        self.writeVInt(0)

        self.writeString(self.player.name) # Имя игрока
        self.writeVInt(0) # Неизвестно
        self.writeVInt(28000000 + self.player.profile_icon) # Иконка профиля
        self.writeVInt(43000000 + self.player.name_color) # Цвет ника
        self.writeVInt(43000000 + self.player.name_color) # Бравл Пассовый цвет ника

        self.writeDataReference(23, self.player.starpower) # Пассивка
        self.writeDataReference(23, self.player.gadget) # Гаджет
        
        self.writeVInt(0) # Массив
        for x in range(0):
            pass
 
        self.writeVInt(0) # Массив
        for x in range(0):
            pass

        self.writeUInt8(0)
        self.writeUInt8(0)

        if self.player.use_gadget:
            self.writeUInt8(6) # 0 = Гаджеты отключены, [1, 3, 5] = Клубные войны (???), [4, 6] = Гаджеты включены  
        else:
            self.writeUInt8(0)