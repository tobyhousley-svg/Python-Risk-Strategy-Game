import random
import time

class Phase():
    def __init__(self, playerarr, player, all_countries, countryarr, popup, UI, adjacency_list):
        self._playerarr = playerarr
        self._player = player
        self._all_countries = all_countries
        self._countryarr = countryarr
        self._popup = popup
        self._UI = UI
        self._opened = False
        self._completed = False
        self._adjacency_list = adjacency_list

    def open_popup(self):
        if not self._opened:
            self._popup.open()
            self._opened = True

    def reset_popup(self):
        self._popup.reset()
        self._opened = False
        self._UI.clear_clicked_country()

class Reinforce(Phase):
    def __init__(self, playerarr, player, all_countries, countryarr, popup, UI, adjacency_list):
        super().__init__(playerarr, player, all_countries, countryarr, popup, UI, adjacency_list)
        self._countries_amnt = len(self._all_countries)
        self._reinforcements = 0
        self._clicked_country = None
        self._got_reinforce_info = False
        self._number = None

    def invalid_turn(self):
        self._reinforcements = 0
        self._popup.reset()
        self._clicked_country = None
        self._got_reinforce_info = False
        self._number = None
        self._UI.clear_clicked_country()
        self._opened = False

    def calc_reinforcements(self):
        countries = len(self._player.get_countries())
        self._reinforcements = countries//3
        if self._reinforcements < 3:
            self._reinforcements = 3
        self._player.set_reinforcements(self._reinforcements)
 
    def set_clicked_country(self,clicked_country):
        if self._player.is_ai():
            self._UI.set_heading("REINFORCE")
            self._UI.set_subheading(f"{self._player.get_name()}'s Turn")
            if self._clicked_country is None:
                chosen = self._player.choose_reinforce_country(self._countryarr, self._adjacency_list)
                if chosen is not None:
                    self._clicked_country = chosen

        else:
            self._UI.set_heading("REINFORCE")
            self._UI.set_subheading(f"Select a country of yours, choose an amount of armies")
            if clicked_country != None:
                self._clicked_country = clicked_country
        
    def reinforce_assign(self):
        if self._clicked_country is None:
            return
        if self._clicked_country.get_name() not in self._player.get_countries():
            self._clicked_country = None 
            return
        if self._player.is_ai():
            armies_num = self._player.choose_reinforce_armies()
            if armies_num is None or armies_num <= 0:
                self._clicked_country = None
                return
            for c in range(len(self._player.get_countries())):
                if self._player.get_countries()[c] == self._clicked_country.get_name():
                    self._player.get_armies()[c] += armies_num
                    self._player.set_reinforcements(self._player.get_reinforcements() - armies_num)

                    self._clicked_country.set_armies(self._player.get_armies()[c])
                    self._clicked_country.update_country(self._playerarr)
                    self._clicked_country = None
                    if self._player.get_reinforcements() == 0:
                        return True
                    else:
                        return

        else:
            if not self._got_reinforce_info:
                self.open_popup()
                if self._popup.get_completed():
                    self._number = self._popup.get_number()
                    if self._number != None and self._number != "":
                        armies_num = int(self._number)
                        if armies_num <= self._reinforcements:
                            self._got_reinforce_info = True
                            for i in range(len(self._player.get_countries())):
                                if self._player.get_countries()[i] == self._clicked_country.get_name():
                                    self._player.get_armies()[i] = self._player.get_armies()[i] + armies_num
                                    self._reinforcements -= armies_num
                                    self._player.set_reinforcements(self._reinforcements)
                                    self._UI.clear_clicked_country()
                                    self._popup.reset()

                                    self._clicked_country.set_armies(self._player.get_armies()[i])
                                    self._clicked_country.update_country(self._playerarr)

                                    self._clicked_country = None
                                    self._got_reinforce_info = False
                                    self._number = None
                                    self._opened = False
                                    if self._reinforcements == 0:
                                        return True
                                    else:
                                        return
                        else:
                            self.reset_popup()
                    else:
                        self._popup.reset()
                        self._opened = False
                        self._clicked_country = None
                        return

class Attack(Phase):
    def __init__(self,playerarr,player,all_countries,countryarr,popup,UI,adjacency_list):
        super().__init__(playerarr,player,all_countries,countryarr,popup,UI,adjacency_list)
        self._got_attacking_country = False
        self._got_defending_country = False
        self._attacked = False
        self._attacking_country = None
        self._defending_country = None

    def done_attacking(self):
        self._UI.set_completed_True()

    def get_countries(self):
        if self._completed == True:
            return
        if self._player.is_ai():
            self._UI.set_heading("ATTACK")
            self._UI.set_subheading(f"{self._player.get_name()}'s Turn")
            try:
                attacking_country,defending_country = self._player.choose_attack_countries(self._adjacency_list, self._countryarr, self)
                self._attacking_country = attacking_country
                self._defending_country = defending_country
                attack_num = self._player.choose_attack_num(self._countryarr,attacking_country)
                if attacking_country != None and defending_country != None and attack_num != None:
                    self.roll_dice(attack_num)
            except:
                return True

            self._attacking_country = attacking_country
            self._defending_country = defending_country
            attack_num = self._player.choose_attack_num(self._countryarr,attacking_country)
            if attack_num == None:
                return True
            if attacking_country != None and defending_country != None and attack_num != None:
                for country in self._countryarr:
                    if country.get_name() == attacking_country:
                        if country.get_armies() > 1:
                            self.roll_dice(attack_num)

        else:
            if not self._got_attacking_country:
                self._UI.set_heading("ATTACK")
                self._UI.set_subheading("Click on the country you want to attack from")
                clicked = self._UI.get_clicked_country_info()
                if clicked in self._player.get_countries():
                    self._attacking_country = clicked
                    self._got_attacking_country = True
                    self._UI.clear_clicked_country()
                print(clicked)

            elif not self._got_defending_country:
                self._UI.set_subheading("Click the country you want to attack, choose how many dice to attack with")
                clicked = self._UI.get_clicked_country_info()
                if clicked and clicked not in self._player.get_countries():
                    if clicked in self._adjacency_list.get(self._attacking_country, []):
                        self._defending_country = clicked
                        self._UI.clear_clicked_country()
                        self._got_defending_country = True
                    else:
                        self.invalid_turn()

            elif not self._attacked:
                self.open_popup()
                if self._popup.get_completed():
                    dice_num = int(self._popup.get_number())
                    attacker_armies = 0
                    for i, c in enumerate(self._player.get_countries()):
                        if c == self._attacking_country:
                            attacker_armies = self._player.get_armies()[i]

                    if 0 < dice_num <= min(3, attacker_armies - 1):
                        self.roll_dice(dice_num)
                        self._opened = False
                    else:
                        self.invalid_turn()

    def invalid_turn(self):
        self._got_attacking_country = False
        self._got_defending_country = False
        self._opened = False
        self._attacked = False
        self._popup.reset()
        self._UI.clear_clicked_country()
        self._attacking_country = None
        self._defending_country = None

    def roll_dice(self,dice_num):
        for c in self._countryarr:
            if c.get_name() == self._attacking_country:
                if dice_num > c.get_armies() - 1:
                    return
        defending_armies = 0
        defender_player = None
        for player in self._playerarr:
            if self._defending_country in player.get_countries():
                defender_player = player
                index = player.get_countries().index(self._defending_country)
                defending_armies = player.get_armies()[index]
                break

        if defending_armies == 0:
            return

        att_rolls = []
        for _ in range(dice_num):
            att_rolls.append(random.randint(1, 6))
        att_rolls.sort(reverse=True)

        def_dice_count = min(2, defending_armies)
        def_rolls = []
        for _ in range(def_dice_count):
            def_rolls.append(random.randint(1, 6))
        def_rolls.sort(reverse=True)

        compare_len = min(len(att_rolls), len(def_rolls))
        att_losses = 0
        def_losses = 0

        for i in range(compare_len):
            if def_rolls[i] >= att_rolls[i]:
                att_losses += 1
            else:
                def_losses += 1

        for i, c in enumerate(self._player.get_countries()):
            if c == self._attacking_country:
                self._player.get_armies()[i] -= att_losses
                attacking_index = i
                for playercountry in self._countryarr:
                    if playercountry.get_name() == self._player.get_countries()[i]:
                        playercountry.set_armies(self._player.get_armies()[i])
                        playercountry.update_country(self._playerarr)
                break

        defender_index = defender_player.get_countries().index(self._defending_country)
        defender_player.get_armies()[defender_index] -= def_losses

        if defender_player.get_armies()[defender_index] <= 0:
            defender_index = defender_player.get_countries().index(self._defending_country)

            defender_player.get_countries().pop(defender_index)
            defender_player.get_armies().pop(defender_index)

            self._player.get_countries().append(self._defending_country)
            self._player.get_armies().append(dice_num - att_losses)


            
            if dice_num <= ((dice_num - att_losses) - 1):
                self._player.get_armies().append(dice_num - att_losses)
                self._player.get_armies()[self._player.get_countries().index(self._attacking_country)] = 1
            else:
                self._player.get_armies().append(dice_num)
                self._player.get_armies()[self._player.get_countries().index(self._attacking_country)] -= dice_num

            for country in self._countryarr:
                if country.get_name() == self._defending_country:
                    print(self._player.get_countries())
                    country.set_armies(self._player.get_armies()[self._player.get_countries().index(self._defending_country)])
                    country.update_country(self._playerarr)
                if country.get_name() == self._attacking_country:
                    print(self._player.get_countries())
                    country.set_armies(self._player.get_armies()[self._player.get_countries().index(self._attacking_country)])
                    country.update_country(self._playerarr)

        self._got_attacking_country = False
        self._got_defending_country = False
        self._opened = False
        self._attacked = False
        self._popup.reset()
        self._UI.clear_clicked_country()
        self._attacking_country = None
        self._defending_country = None

        time.sleep(0.5)

    def is_completed(self):
        return self._completed

class Fortify(Phase):
    def __init__(self,playerarr,player,all_countries,countryarr,popup,UI,adjacency_list):
        super().__init__(playerarr,player,all_countries,countryarr,popup,UI,adjacency_list)
        self._got_move_from = False
        self._got_move_to = False
        self._got_country_from = False
        self._got_country_to = False
        self._from_country = None
        self._to_country = None
        self._available_armies = 0

    def invalid_turn(self):
        self._got_move_from = False
        self._got_move_to = False
        self._opened = False
        self._got_country_from = False
        self._got_country_to = False
        self._from_country = None
        self._to_country = None
        self._available_armies = 0
        self._moving_num = 0

    def get_countries(self):
        if self._completed == True:
            return
        if self._player.is_ai():
            self._UI.set_heading("FORTIFY")
            self._UI.set_subheading(f"{self._player.get_name()}'s Turn")
            if self._player.fortify_operations(self._adjacency_list, self._countryarr, self._playerarr):
                return True
        else:
            self._UI.set_heading("FORTIFY")
            self._UI.set_subheading(f"Select the countries you'd like to reinforce from, and to")
            if not self._got_country_from:
                self._from_country = self._UI.get_clicked_country_info()
                if self._from_country in self._player.get_countries():
                    self._got_country_from = True
                    self._UI.clear_clicked_country()
            if self._got_country_from:
                for country in self._countryarr:
                    if country.get_name() == self._from_country:
                        if country.get_armies() > 1:
                            if self._got_country_to != True:
                                self._to_country = self._UI.get_clicked_country_info()
                                if self._to_country in self._player.get_countries():
                                    self._UI.clear_clicked_country()
                                    if self._to_country in self._adjacency_list[self._from_country]:
                                        self._got_country_to = True
                        else:
                            self.invalid_turn()

            if self._got_country_to == True:  
                self.open_popup()
                if self._popup.get_completed():
                    if self._popup.get_number() != None and self._popup.get_number() != "":
                        self._moving_num = self._popup.get_number()
                        self._moving_num = int(self._moving_num)
                        if self._moving_num > 0 and self._moving_num < self._player.get_armies()[self._player.get_countries().index(self._from_country)]:
                            if self._completed != True:
                                self.move_armies()
                            else:
                                return True
                        else:
                            self.invalid_turn()
                    else:
                        self.invalid_turn()

            if self._completed == True:
                
                return True

    def move_armies(self):
        for index,country in enumerate(self._player.get_countries()):
            if country == self._from_country:
                self._player.get_armies()[index] -= self._moving_num
                for c in self._countryarr:
                    if c.get_name() == self._from_country:
                        c.set_armies(self._player.get_armies()[index])
                        c.update_country(self._playerarr)
            if country == self._to_country:
                self._player.get_armies()[index] += self._moving_num
                for c in self._countryarr:
                    if c.get_name() == self._to_country:
                        c.set_armies(self._player.get_armies()[index])
                        c.update_country(self._playerarr)
        self._completed = True
