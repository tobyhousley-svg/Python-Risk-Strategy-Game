import os
import pygame
import random
import json

from Players import Player, AI_Player
from UI import Userinterface

DIRPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRPATH = str(DIRPATH)
WIDTH = 1800
HEIGHT = 980
CLOCK = pygame.time.Clock()

class Game:
    def __init__(self, playernum,all_countries, UI):
        self.__neutral = False
        self.__playernum = playernum
        if self.__playernum == 2:
            self.__playernum = 3
            self.__neutral = True
        self.__playerarr = []
        self.__colourarr = [(255,0,0),(0,0,255),(255,165,0),(128,0,128),(4,46,96)]
        self.__all_countries = all_countries
        self.__UI = UI

        self.__countriesarr = list(self.__all_countries.keys())

    def assign_player_info(self, game_name):
        countries_each = len(self.__countriesarr) // self.__playernum
        remaining_countries = len(self.__countriesarr) % self.__playernum

        for i in range(self.__playernum):
            player_countries = []
            if self.__neutral == True and i == 2:
                name = "Neutral"
                colour = (150,150,150)
            else:
                if i == 0:
                    name = "You"
                    colour = (0, 255, 0)
                else:
                    name = "AI" + str(i)
                    colour = random.choice(self.__colourarr)
                    self.__colourarr.remove(colour)

            for n in range(countries_each):
                country = random.choice(self.__countriesarr)
                player_countries.append(country)
                self.__countriesarr.remove(country)
            if remaining_countries > 0:
                country = random.choice(self.__countriesarr)
                player_countries.append(country)
                self.__countriesarr.remove(country)
                remaining_countries = remaining_countries - 1

            armies = []
            for n in range(len(player_countries)):
                armies.append(1)

            if i == 0:
                newplayer = Player(name, colour, player_countries, armies, reinforcements=0)
            else:
                newplayer = AI_Player(name, colour, player_countries, armies, reinforcements=0)
            self.__playerarr.append(newplayer)


        save_data = {
            "game_state": {
                "phase": "reinforce",
                "current_player_index": 0,
                "heading": "",
                "subheading": "",

            },
            "players": []
        }
        
        for player in self.__playerarr:
            save_data["players"].append(self.convert_player_dict(player))


        filepath = (DIRPATH+f"/{game_name}.json")
        with open(filepath, "w") as file:
            json.dump(save_data, file, indent=4)

        return self.__playerarr
    
    def convert_player_dict(self,player):
        return{
            "name": player.get_name(),
            "colour": player.get_colour(),
            "countries": player.get_countries(),
            "armies": player.get_armies(),
            "reinforcements": player.get_reinforcements()
        }

    def save_game(self, playerarr, game_name, heading, subheading, phase, player_index):
        for filename in os.listdir(DIRPATH):
            if filename == f"{game_name}.json":
                save_data = {
                    "game_state": {
                        "phase": phase,
                        "current_player_index": player_index,
                        "heading": heading,
                        "subheading": subheading,
                    },
                    "players": []
                }
                for player in playerarr:
                    save_data["players"].append(self.convert_player_dict(player))

                filepath = (DIRPATH+f"/{game_name}.json")
                with open(filepath, "w") as file:
                    json.dump(save_data, file, indent=4)

    def load_player_info(self, game_to_open):
        playerarr = []
        filepath = (DIRPATH+f"/{game_to_open}.json")
        with open(filepath, "r") as file:
            data = json.load(file)
            for i, player in enumerate(data["players"]):
                name = player["name"]
                colour = tuple(player["colour"])
                countries = player["countries"]
                armies = player["armies"]
                reinforcements = player["reinforcements"]

                if name == "You":
                    newplayer = Player(name,colour,countries,armies,reinforcements)
                else:
                    newplayer = AI_Player(name,colour,countries,armies,reinforcements)
                
                playerarr.append(newplayer)

            phase = data["game_state"]["phase"]
            player_index = data["game_state"]["current_player_index"]
            heading = data["game_state"]["heading"]
            subheading = data["game_state"]["subheading"]

        return playerarr, phase, player_index, heading, subheading, game_to_open

def main():
    x_offset = 15
    y_offset = 60
    all_countries = {
        'Alaska': (os.path.join(DIRPATH, 'countries', '1x', 'Alaska.png'), (117+ x_offset, 96+ y_offset)),
        'NorthernTerritory': (os.path.join(DIRPATH, 'countries', '1x', 'NorthernTerritory.png'), (217+ x_offset, 73+ y_offset)),
        'Greenland': (os.path.join(DIRPATH, 'countries', '1x', 'Greenland.png'), (450+ x_offset, 35+ y_offset)),
        'Alberta': (os.path.join(DIRPATH, 'countries', '1x', 'Alberta.png'), (230+ x_offset, 172+ y_offset)),
        'Ontario': (os.path.join(DIRPATH, 'countries', '1x', 'Ontario.png'), (327+ x_offset, 175+ y_offset)),
        'Quebec': (os.path.join(DIRPATH, 'countries', '1x', 'Quebec.png'), (402+ x_offset, 165+ y_offset)),
        'WesternUnitedStates': (os.path.join(DIRPATH, 'countries', '1x', 'WesternUnitedStates.png'), (233+ x_offset, 256+ y_offset)),
        'EasternUnitedStates': (os.path.join(DIRPATH, 'countries', '1x', 'EasternUnitedStates.png'), (306+ x_offset, 256+ y_offset)),
        'CentralAmerica': (os.path.join(DIRPATH, 'countries', '1x', 'CentralAmerica.png'), (243+ x_offset,348+ y_offset)),
        'Venezuela': (os.path.join(DIRPATH, 'countries', '1x', 'Venezuela.png'), (328+ x_offset, 450+ y_offset)),
        'Peru': (os.path.join(DIRPATH, 'countries', '1x', 'Peru.png'), (313+ x_offset, 505+ y_offset)),
        'Brazil': (os.path.join(DIRPATH, 'countries', '1x', 'Brazil.png'), (352+ x_offset, 491+ y_offset)),
        'Argentina': (os.path.join(DIRPATH, 'countries', '1x', 'Argentina.png'), (370+ x_offset, 615+ y_offset)),
        'Iceland': (os.path.join(DIRPATH, 'countries', '1x', 'Iceland.png'), (570+ x_offset, 180+ y_offset)),
        'Scandinavia': (os.path.join(DIRPATH, 'countries', '1x', 'Scandinavia.png'), (708+ x_offset, 147+ y_offset)),
        'GreatBritain': (os.path.join(DIRPATH, 'countries', '1x', 'GreatBritain.png'), (570+ x_offset, 250+ y_offset)),
        'NorthernEurope': (os.path.join(DIRPATH, 'countries', '1x', 'NorthernEurope.png'), (692+ x_offset, 275+ y_offset)),
        'WesternEurope': (os.path.join(DIRPATH, 'countries', '1x', 'WesternEurope.png'), (610+ x_offset, 365+ y_offset)),
        'SouthernEurope': (os.path.join(DIRPATH, 'countries', '1x', 'SouthernEurope.png'), (703+ x_offset, 364+ y_offset)),
        'Ukraine': (os.path.join(DIRPATH, 'countries', '1x', 'Ukraine.png'), (787+ x_offset, 150+ y_offset)),
        'NorthAfrica': (os.path.join(DIRPATH, 'countries', '1x', 'NorthAfrica.png'), (620+ x_offset, 495+ y_offset)),
        'Egypt': (os.path.join(DIRPATH, 'countries', '1x', 'Egypt.png'), (750+ x_offset, 520+ y_offset)),
        'EastAfrica': (os.path.join(DIRPATH, 'countries', '1x', 'EastAfrica.png'), (809+ x_offset, 587+ y_offset)),
        'Congo': (os.path.join(DIRPATH, 'countries', '1x', 'Congo.png'), (745+ x_offset, 650+ y_offset)),
        'SouthAfrica': (os.path.join(DIRPATH, 'countries', '1x', 'SouthAfrica.png'), (756+ x_offset, 736+ y_offset)),
        'Madagascar': (os.path.join(DIRPATH, 'countries', '1x', 'Madagascar.png'), (890+ x_offset, 780+ y_offset)),
        'Ural': (os.path.join(DIRPATH, 'countries', '1x', 'Ural.png'), (963+ x_offset, 113+ y_offset)),
        'Serbia': (os.path.join(DIRPATH, 'countries', '1x', 'Serbia.png'), (995+ x_offset, 71+ y_offset)),
        'Yakutsk': (os.path.join(DIRPATH, 'countries', '1x', 'Yakutsk.png'), (1119+ x_offset, 92+ y_offset)),
        'Kamchatka': (os.path.join(DIRPATH, 'countries', '1x', 'Kamchatka.png'), (1190+ x_offset, 110+ y_offset)),
        'Irkutsk': (os.path.join(DIRPATH, 'countries', '1x', 'Irkutsk.png'), (1092+ x_offset, 196+ y_offset)),
        'Mongolia': (os.path.join(DIRPATH, 'countries', '1x', 'Mongolia.png'), (1107+ x_offset, 277+ y_offset)),
        'Japan': (os.path.join(DIRPATH, 'countries', '1x', 'Japan.png'), (1270+ x_offset, 280+ y_offset)),
        'China': (os.path.join(DIRPATH, 'countries', '1x', 'China.png'), (1032+ x_offset, 324+ y_offset)),
        'MiddleEast': (os.path.join(DIRPATH, 'countries', '1x', 'MiddleEast.png'), (803+ x_offset, 430+ y_offset)),
        'Afghanistan': (os.path.join(DIRPATH, 'countries', '1x', 'Afghanistan.png'), (906+ x_offset, 296+ y_offset)),
        'India': (os.path.join(DIRPATH, 'countries', '1x', 'India.png'), (983+ x_offset, 420+ y_offset)),
        'Siam': (os.path.join(DIRPATH, 'countries', '1x', 'Siam.png'), (1117+ x_offset, 490+ y_offset)),
        'Indonesia': (os.path.join(DIRPATH, 'countries', '1x', 'Indonesia.png'), (1100+ x_offset, 640+ y_offset)),
        'NewGuinea': (os.path.join(DIRPATH, 'countries', '1x', 'NewGuinea.png'), (1250+ x_offset, 630+ y_offset)),
        'WesternAustralia': (os.path.join(DIRPATH, 'countries', '1x', 'WesternAustralia.png'), (1180+ x_offset, 730+ y_offset)),
        'EasternAustralia': (os.path.join(DIRPATH, 'countries', '1x', 'EasternAustralia.png'), (1274+ x_offset, 720+ y_offset)),
    }
    
    adjacency_list = {
        # --- North America ---
        "Alaska": ["NorthernTerritory", "Alberta", "Kamchatka"],
        "NorthernTerritory": ["Alaska", "Alberta", "Ontario", "Greenland"],
        "Greenland": ["NorthernTerritory", "Ontario", "Quebec", "Iceland"],
        "Alberta": ["Alaska", "NorthernTerritory", "Ontario", "WesternUnitedStates"],
        "Ontario": ["NorthernTerritory", "Greenland", "Quebec", "EasternUnitedStates", "WesternUnitedStates", "Alberta"],
        "Quebec": ["Ontario", "Greenland", "EasternUnitedStates"],
        "WesternUnitedStates": ["Alberta", "Ontario", "EasternUnitedStates", "CentralAmerica"],
        "EasternUnitedStates": ["WesternUnitedStates", "Ontario", "Quebec", "CentralAmerica"],
        "CentralAmerica": ["WesternUnitedStates", "EasternUnitedStates", "Venezuela"],

        # --- South America ---
        "Venezuela": ["CentralAmerica", "Brazil", "Peru"],
        "Peru": ["Venezuela", "Brazil", "Argentina"],
        "Brazil": ["Venezuela", "Peru", "Argentina", "NorthAfrica"],
        "Argentina": ["Peru", "Brazil"],

        # --- Europe ---
        "Iceland": ["Greenland", "Scandinavia", "GreatBritain"],
        "Scandinavia": ["Iceland", "NorthernEurope", "Ukraine", "GreatBritain"],
        "GreatBritain": ["Iceland", "Scandinavia", "NorthernEurope", "WesternEurope"],
        "NorthernEurope": ["GreatBritain", "Scandinavia", "Ukraine", "SouthernEurope", "WesternEurope"],
        "WesternEurope": ["GreatBritain", "NorthernEurope", "SouthernEurope", "NorthAfrica"],
        "SouthernEurope": ["WesternEurope", "NorthernEurope", "Ukraine", "Egypt", "MiddleEast", "NorthAfrica"],
        "Ukraine": ["Scandinavia", "NorthernEurope", "SouthernEurope", "Ural", "Afghanistan", "MiddleEast"],

        # --- Africa ---
        "NorthAfrica": ["Brazil", "WesternEurope", "SouthernEurope", "Egypt", "EastAfrica", "Congo"],
        "Egypt": ["SouthernEurope", "MiddleEast", "EastAfrica", "NorthAfrica"],
        "EastAfrica": ["Egypt", "MiddleEast", "Madagascar", "SouthAfrica", "Congo", "NorthAfrica"],
        "Congo": ["NorthAfrica", "EastAfrica", "SouthAfrica"],
        "SouthAfrica": ["Congo", "EastAfrica", "Madagascar"],
        "Madagascar": ["EastAfrica", "SouthAfrica"],

        # --- Asia ---
        "Ural": ["Ukraine", "Serbia", "China", "Afghanistan"],
        "Serbia": ["Ural", "Yakutsk", "Irkutsk", "Mongolia", "China"],
        "Yakutsk": ["Serbia", "Kamchatka", "Irkutsk"],
        "Kamchatka": ["Yakutsk", "Irkutsk", "Mongolia", "Japan", "Alaska"],
        "Irkutsk": ["Serbia", "Yakutsk", "Kamchatka", "Mongolia"],
        "Mongolia": ["Serbia", "Irkutsk", "Kamchatka", "Japan", "China"],
        "Japan": ["Kamchatka", "Mongolia"],
        "China": ["Ural", "Serbia", "Mongolia", "Siam", "India", "Afghanistan"],
        "MiddleEast": ["SouthernEurope", "Ukraine", "Afghanistan", "India", "EastAfrica", "Egypt"],
        "Afghanistan": ["Ukraine", "Ural", "China", "India", "MiddleEast"],
        "India": ["MiddleEast", "Afghanistan", "China", "Siam"],
        "Siam": ["India", "China", "Indonesia"],

        # --- Australia ---
        "Indonesia": ["Siam", "NewGuinea", "WesternAustralia"],
        "NewGuinea": ["Indonesia", "EasternAustralia"],
        "WesternAustralia": ["Indonesia", "EasternAustralia"],
        "EasternAustralia": ["WesternAustralia", "NewGuinea"],
    }

    while True:
        newUI = Userinterface(all_countries,adjacency_list)
        playernum, game_name, load_game_name = newUI.menu_loop()
        newgame = Game(playernum,all_countries, newUI)
        if playernum == 0:
            playerarr, phase, player_index, heading, subheading, loaded_game_name = newgame.load_player_info(load_game_name)
            newUI.set_game_name(loaded_game_name)
        else:
            playerarr = newgame.assign_player_info(game_name)

        newUI.set_game(newgame)
        newUI.set_playerarr(playerarr)
        if playernum == 0:
            newUI.set_game_phase(phase, player_index, heading, subheading)
        newUI.game_loop()

main()
