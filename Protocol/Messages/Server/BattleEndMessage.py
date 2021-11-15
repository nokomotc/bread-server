from ByteStream.Writer import Writer
import json
from DataBase.MongoDB import MongoDB

class BattleEndMessage(Writer):

    def __init__(self, client, player, type, result, players):
        super().__init__(client)
        self.id = 23456
        self.player  = player
        self.type    = type
        self.result  = result
        self.players = players

    def encode(self):
        self.config = json.loads(open('config.json', 'r').read())
        self.db = MongoDB(self.config['MongoConnectionURL'])
        result = 16
        brawler_trophies = self.player.brawlers_trophies[str(self.player.home_brawler)]
        brawler_trophies_for_rank = self.player.brawlers_high_trophies[str(self.player.home_brawler)]
        brawler_level = self.player.brawlers_level[str(self.player.home_brawler)] + 1
        rank_1_val = 10
        rank_2_val = 0
        rank_3_val = 0
        rank_4_val = 0
        rank_5_val = 0
        rank_6_val = 0
        rank_7_val = 0
        rank_8_val = 0
        rank_9_val = 0
        rank_10_val = 0

        # Rewards
        exp_reward = [15, 12, 9, 6, 5, 4, 3, 2, 1, 0]
        token_list = [34, 28, 22, 16, 12, 8, 6, 4, 2, 0]
        practice_exp_reward = [8, 6, 5, 3, 3, 2, 2, 1, 1, 0] 
        practice_token_list = [17, 14, 11, 8, 6, 4, 3, 2, 1, 0]
        mvp_exp_reward = [10]
        # Trophy Balance
        if 0 <= brawler_trophies <= 49:
            rank_1_val = 10
            rank_2_val = 8
            rank_3_val = 7
            rank_4_val = 6
            rank_5_val = 4
            rank_6_val = 2
            rank_7_val = 2
            rank_8_val = 1
            rank_9_val = 0
            rank_10_val = 0
        else:
            if 50 <= brawler_trophies <= 99:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 7
                rank_4_val = 6
                rank_5_val = 3
                rank_6_val = 2
                rank_7_val = 2
                rank_8_val = 0
                rank_9_val = -1
                rank_10_val = -2
            if 100 <= brawler_trophies <= 199:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 7
                rank_4_val = 6
                rank_5_val = 3
                rank_6_val = 1
                rank_7_val = 0
                rank_8_val = -1
                rank_9_val = -2
                rank_10_val = -2
            if 200 <= brawler_trophies <= 299:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 6
                rank_4_val = 5
                rank_5_val = 3
                rank_6_val = 1
                rank_7_val = 0
                rank_8_val = -2
                rank_9_val = -3
                rank_10_val = -3
            if 300 <= brawler_trophies <= 399:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 6
                rank_4_val = 5
                rank_5_val = 2
                rank_6_val = 0
                rank_7_val = 0
                rank_8_val = -3
                rank_9_val = -4
                rank_10_val = -4
            if 400 <= brawler_trophies <= 499:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 6
                rank_4_val = 5
                rank_5_val = 2
                rank_6_val = -1
                rank_7_val = -2
                rank_8_val = -3
                rank_9_val = -5
                rank_10_val = -5
            if 500 <= brawler_trophies <= 599:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 6
                rank_4_val = 4
                rank_5_val = 2
                rank_6_val = -1
                rank_7_val = -2
                rank_8_val = -5
                rank_9_val = -6
                rank_10_val = -6
            if 600 <= brawler_trophies <= 699:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 6
                rank_4_val = 4
                rank_5_val = 1
                rank_6_val = -2
                rank_7_val = -2
                rank_8_val = -5
                rank_9_val = -7
                rank_10_val = -8
            if 700 <= brawler_trophies <= 799:
                rank_1_val = 10
                rank_2_val = 8
                rank_3_val = 6
                rank_4_val = 4
                rank_5_val = 1
                rank_6_val = -3
                rank_7_val = -4
                rank_8_val = -5
                rank_9_val = -8
                rank_10_val = -9
            if 800 <= brawler_trophies <= 899:
                rank_1_val = 9
                rank_2_val = 7
                rank_3_val = 5
                rank_4_val = 2
                rank_5_val = 0
                rank_6_val = -3
                rank_7_val = -4
                rank_8_val = -7
                rank_9_val = -9
                rank_10_val = -10
            if 900 <= brawler_trophies <= 999:
                rank_1_val = 8
                rank_2_val = 6
                rank_3_val = 4
                rank_4_val = 1
                rank_5_val = -1
                rank_6_val = -3
                rank_7_val = -6
                rank_8_val = -8
                rank_9_val = -10
                rank_10_val = -11
            if 1000 <= brawler_trophies <= 1099:
                rank_1_val = 6
                rank_2_val = 5
                rank_3_val = 3
                rank_4_val = 1
                rank_5_val = -2
                rank_6_val = -5
                rank_7_val = -6
                rank_8_val = -9
                rank_9_val = -11
                rank_10_val = -12
            if 1100 <= brawler_trophies <= 1199:
                rank_1_val = 5
                rank_2_val = 4
                rank_3_val = 1
                rank_4_val = 0
                rank_5_val = -2
                rank_6_val = -6
                rank_7_val = -7
                rank_8_val = -10
                rank_9_val = -12
                rank_10_val = -13
            if brawler_trophies >= 1200:
                rank_1_val = 5
                rank_2_val = 3
                rank_3_val = 0
                rank_4_val = -1
                rank_5_val = -2
                rank_6_val = -6
                rank_7_val = -8
                rank_8_val = -11
                rank_9_val = -12
                rank_10_val = -13
                
        # Result Rewards 
        if self.result == 1:
            gainedtokens = token_list[0]
            gainedexperience = exp_reward[0]
            gainedtrophies = rank_1_val
                #self.player.solo_wins += 1
                #db.update_player_account(self, 'soloWins', self.player.solo_wins)
        if self.result == 2:
                gainedtokens = token_list[1]
                gainedexperience = exp_reward[1]
                gainedtrophies = rank_2_val
        if self.result == 3:
                gainedtokens = token_list[2]
                gainedexperience = exp_reward[2]
                gainedtrophies = rank_3_val
        if self.result == 4:
                gainedtokens = token_list[3]
                gainedexperience = exp_reward[3]
                gainedtrophies = rank_4_val
        if self.result == 5:
                gainedtokens = token_list[4]
                gainedexperience = exp_reward[4]
                gainedtrophies = rank_5_val
        if self.result == 6:
                gainedtokens = token_list[5]
                gainedexperience = exp_reward[5]
                gainedtrophies = rank_6_val
        if self.result == 7:
                gainedtokens = token_list[6]
                gainedexperience = exp_reward[6]
                gainedtrophies = rank_6_val
        if self.result == 8:
                gainedtokens = token_list[7]
                gainedexperience = exp_reward[7]
                gainedtrophies = rank_8_val
        if self.result == 9:
                gainedtokens = token_list[8]
                gainedexperience = exp_reward[8]
                gainedtrophies = rank_9_val
        if self.result == 10:
                gainedtokens = token_list[9]
                gainedexperience = exp_reward[9]
                gainedtrophies = rank_10_val
                
        starplayer = 0
        # Star Player Info
        if starplayer == 5:
            starplayerexperience = mvp_exp_reward[0]
        else:
            starplayerexperience = 0
        # Results Balance
        if result in [0, 1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 19, 24, 25, 26, 27]:
            tokens = gainedtokens
        if result in [4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31]:
            tokens = 0
        if result in [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29]:
            mvpexperience = starplayerexperience
            experience = gainedexperience
        if result in [2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31]:
            mvpexperience = 0
            experience = 0
        if result in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]:
            startoken = 1
        if result in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]:
            startoken = 0
        if 0 <= result <= 31:
            trophies = gainedtrophies
        token = tokens    
        # DataBase Stuff            
        self.player.exp_points += experience + mvpexperience
        if self.player.double_token_event:
            double_token_event = token
        else:
            double_token_event = 0
        if self.player.token_doubler <= 0:
            doubledtokens = 0
        if self.player.token_doubler > token + double_token_event:
            doubledtokens = token + double_token_event
        if token + double_token_event >= self.player.token_doubler: 
            doubledtokens = self.player.token_doubler
        remainingtokens = (self.player.token_doubler) - doubledtokens
        totaltokens = token + double_token_event + doubledtokens
        if self.player.coin_shower_event:
            coinevent = totaltokens
        else:
            coinevent = 0
        new_gold = self.player.resources[1]['Amount'] + coinevent
        new_trophies = self.player.trophies + trophies
        new_tokens = self.player.resources[0]['Amount'] + totaltokens
        new_startokens = self.player.resources[2]['Amount'] + startoken
        self.player.brawlers_trophies[str(self.player.home_brawler)] = brawler_trophies + trophies
        if self.player.brawlers_high_trophies[str(self.player.home_brawler)] < self.player.brawlers_trophies[str(self.player.home_brawler)]:
            self.player.brawlers_high_trophies[str(self.player.home_brawler)] = brawler_trophies_for_rank - brawler_trophies_for_rank + brawler_trophies + trophies

        self.player.resources[0]['Amount'] = new_tokens
        self.player.resources[1]['Amount'] = new_gold
        self.player.resources[2]['Amount'] = new_startokens

        self.db.update_player_account(self.player.token, 'BrawlersTrophies', self.player.brawlers_trophies)
        self.db.update_player_account(self.player.token, 'BrawlersHighestTrophies', self.player.brawlers_high_trophies)
        self.db.update_player_account(self.player.token, 'BrawlersHighestTrophies', self.player.brawlers_high_trophies)
        self.db.update_player_account(self.player.token, 'Trophies', new_trophies)
        self.db.update_player_account(self.player.token, 'TokenDoubler', remainingtokens)
        self.db.update_player_account(self.player.token, 'ExperiencePoints', self.player.exp_points)
        self.db.update_player_account(self.player.token, 'Resources', self.player.resources)
            
        self.writeVInt(self.type) # Battle End Game Mode 
        self.writeVInt(self.result) # Result 
        self.writeVInt(token) # Tokens Gained
        if result < 16:
            self.writeVInt(0) # Trophies Result 
        if result >= 16:
            if gainedtrophies >= 0:
                self.writeVInt(gainedtrophies) # Trophies Result
            if gainedtrophies < 0:
                self.writeVInt(-65 - (gainedtrophies)) # Trophies Result
        self.writeVInt(0) # Unknown (Power Play Related)
        self.writeVInt(doubledtokens) # Doubled Tokens
        self.writeVInt(double_token_event) # Double Token Event
        self.writeVInt(remainingtokens) # Token Doubler Remaining
        self.writeVInt(0) # Big Game/Robo Rumble Time
        self.writeVInt(0) # Unknown (Championship Related)
        self.writeVInt(0) # Championship Level Passed
        self.writeVInt(0) # Challenge Reward Type (0 = Star Points, 1 = Star Tokens)
        self.writeVInt(0) # Challenge Reward Ammount
        self.writeVInt(0) # Championship Losses Left
        self.writeVInt(0) # Championship Maximun Losses
        self.writeVInt(coinevent) # Coin Shower Event
        self.writeVInt(0) # Underdog Trophies
        self.writeVInt(16) # Battle Result Type
        self.writeVInt(-64) # Championship Challenge Type
        self.writeVInt(1) # Championship Cleared and Beta Quests
        
        # Players Array
        self.writeVInt(1) # Battle End Screen Players
        
        self.writeVInt(1) # Player Team and Star Player Type
        self.writeDataReference(16, self.player.home_brawler) # Player Brawler
        self.writeDataReference(29, self.player.selected_skins[str(self.player.home_brawler)]) # Player Skin
        self.writeVInt(brawler_trophies) # Brawler Trophies
        self.writeVInt(brawler_trophies_for_rank) # Player Power Play Points
        self.writeVInt(brawler_level) # Brawler Power Level
        self.writeBoolean(True) # Player HighID and LowID Array
        self.writeInt(0) # HighID
        self.writeInt(1) # LowID
        self.writeString(self.player.name) # Имя игрока
        self.writeVInt(0)
        self.writeVInt(28000000 + self.player.profile_icon) # Иконка игрока
        self.writeVInt(43000000 + self.player.name_color) # Цвет имени
        if self.player.bp_activated:
            self.writeVInt(43000000 + self.player.name_color) # Градиентный цвет имени (Brawl Pass)
        else:
            self.writeVInt(0) # Градиентный цвет имени (Brawl Pass)
        
        # Experience Array
        self.writeVInt(2) # Count
        self.writeVInt(0) # Normal Experience ID
        self.writeVInt(experience) # Normal Experience Gained
        self.writeVInt(8) # Star Player Experience ID
        self.writeVInt(mvpexperience) # Star Player Experience Gained

        # Rank Up and Level Up Bonus Array
        self.writeVInt(0) # Count

        # Trophies and Experience Bars Array
        self.writeVInt(2) # Count
        self.writeVInt(1) # Trophies Bar Milestone ID
        self.writeVInt(brawler_trophies) # Brawler Trophies
        self.writeVInt(brawler_trophies_for_rank) # Brawler Trophies for Rank
        self.writeVInt(5) # Experience Bar Milestone ID
        self.writeVInt(self.player.exp_points -experience -mvpexperience) # Player Experience
        self.writeVInt(self.player.exp_points -experience -mvpexperience) # Player Experience for Level
        
        self.writeDataReference(28, self.player.profile_icon)  # Player Profile Icon (Unused since 2017)
        self.writeBoolean(False)  # Play Again
            
        self.writeVInt(1)

        self.writeVInt(4)
        self.writeVInt(4)
        self.writeVInt(2) # Mission type
        self.writeVInt(0)  # Current goal achieve
        self.writeVInt(8)  # Quest goal
        self.writeVInt(500)  # Tokens reward
        self.writeVInt(2)
        self.writeVInt(0) # Current level + 1 in game
        self.writeVInt(0) # Max level
        self.writeVInt(2)
        self.writeUInt8(0)  # Is brawl pass exclusive

        self.writeDataReference(16, 0)

        self.writeVInt(0) # Gamemode TID
        self.writeVInt(5)
        self.writeVInt(5)