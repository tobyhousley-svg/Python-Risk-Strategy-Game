import pygame
import random
import os
import sys
import time

from Phases import Reinforce, Attack, Fortify

DIRPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRPATH = str(DIRPATH)
WIDTH = 1800
HEIGHT = 980
CLOCK = pygame.time.Clock()

class Country_Class():
    def __init__ (self,name,image_directory,position,playerarr,mouse_pos):
        self._name = name
        self._ownership = ""
        self._image_directory = image_directory
        self._position = position
        self._armies = 0
        self._colour = 0,0,0
        self.__base_font = pygame.font.Font(None,35)
        self.__playerarr = playerarr
        for i in range (len(playerarr)):
            if self._name in self.__playerarr[i].get_countries():
                self._colour = self.__playerarr[i].get_colour()
                self._ownership = self.__playerarr[i].get_name()
                for n in range (len(playerarr[i].get_countries())):
                    if playerarr[i].get_countries()[n] == self._name:
                        self._armies = self.__playerarr[i].get_armies()[n]

        self.__ArmyNumSurface = self.__base_font.render(f"{self._armies}",True,(000,000,000))

        self.__country_image = pygame.image.load(self._image_directory).convert_alpha()

        self.__image_scale = 0.8
        self.__image_width = self.__country_image.get_width()
        self.__image_height = self.__country_image.get_height()
        self.__country_image = pygame.transform.scale(self.__country_image,(int(self.__image_width*self.__image_scale),(int(self.__image_height*self.__image_scale))))

        self.__country_rect = self.__country_image.get_rect(topleft=self._position)
        self.__mouse_pos = mouse_pos

        self.apply_colour()
        
    def set_armies(self,armies):
        self._armies = armies

    def update_country(self,playerarr):
        for player in playerarr:
            if self._name in player.get_countries():
                self._ownership = player.get_name()
                self._colour = player.get_colour()

                self.__ArmyNumSurface = self.__base_font.render(f"{self._armies}",True,(000,000,000))

                self.__country_image = pygame.image.load(self._image_directory).convert_alpha()
                self.__country_image = pygame.transform.scale(self.__country_image,(int(self.__image_width*self.__image_scale),(int(self.__image_height*self.__image_scale))))

                self.apply_colour()

    def check_clicked (self):
        if self.__country_rect.collidepoint(self.__mouse_pos):
            mouseX = self.__mouse_pos[0] - self._position[0]
            mouseY = self.__mouse_pos[1] - self._position[1]
            if (0 <= mouseX < self.__country_image.get_width() and 0 <= mouseY < self.__country_image.get_height()):
                try:
                    pixel_alpha = self.__country_image.get_at((mouseX, mouseY))[3]
                    if pixel_alpha > 0:
                        return True
                except:
                    pass
        return False

    def update_mouse_pos (self,mouse_pos):
        self.__mouse_pos = mouse_pos

    def draw_country (self,screen):
        screen.blit(self.__country_image,(self._position))
        pos_x = self._position[0] + ((self.__image_width * self.__image_scale) / 2) - 3
        pos_y = self._position[1] + ((self.__image_height * self.__image_scale) / 2) - 7
        position = (pos_x,pos_y)
        screen.blit(self.__ArmyNumSurface, (position))                  

    def apply_colour(self):
        img = self.__country_image.copy()
        px = pygame.PixelArray(img)

        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.unmap_rgb(px[x, y])

                if r >= 200 and g >= 200 and b >= 200 and a > 0:
                    px[x, y] = self._colour
                if r <= 100 and g <= 100 and b <= 100 and a > 0:
                    px[x,y] = (255,255,255)

        px.close()
        self.__country_image = img

    def get_name(self):
        return self._name
    
    def get_armies(self):
        return self._armies

    def __str__ (self):
        return (f"name = {self._name}, image directory = {self._image_directory}, position: {self._position}")

class Button():
    def __init__(self,screen,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self._image = pygame.transform.scale(image,(int(width*scale),(int(height*scale))))
        self._rect = self._image.get_rect()
        self._rect.topleft = (x,y)
        self._screen = screen
        self._clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self._rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if self._clicked == False:
                    self._clicked = True
            elif pygame.mouse.get_pressed()[0] == 0:
                if self._clicked == True:
                    self._clicked = False
                    action = True
        else:
            if pygame.mouse.get_pressed()[0] == 0:
                self._clicked = False

        self._screen.blit(self._image, (self._rect.x,self._rect.y))
        return action

class Slider():
    def __init__(self, screen):
        self._screen = screen

        self._slider_line_length = 400
        self._slider_line_colour = (0,0,0)

        self._slider_width = 20
        self._slider_height = 40
        self._slider_colour = (255,0,0)

        self._slider_x = (WIDTH/2) - (self._slider_line_length/2)
        self._slider_y = 440

        self._slider_mech_x = self._slider_x

        self._slider_interval_amount = 5
        self._distance_between_intervals = self._slider_line_length / (self._slider_interval_amount - 1)
        self._interval_array = []
        for i in range(self._slider_interval_amount):
            interval = self._slider_x + (i * self._distance_between_intervals)
            self._interval_array.append(interval)

        self._closest_interval = self._interval_array[0]

    def mouse_held(self):
        mouse_buttons = pygame.mouse.get_pressed()
        left_held = mouse_buttons[0]
        return left_held
    
    def calc_slider(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.mouse_held():
            if mouse_pos[0] > self._slider_x and mouse_pos[0] < (self._slider_x + self._slider_line_length):
                if mouse_pos[1] > (self._slider_y - 45) and mouse_pos[1] < (self._slider_y + 45):

                    self._closest_interval = 0
                    biggest_distance = 99999
                    for interval in self._interval_array:
                        distance = abs(interval - mouse_pos[0])
                        if distance < biggest_distance:
                            biggest_distance = distance
                            self._closest_interval = interval
                    self._slider_mech_x = self._closest_interval
        return self._interval_array.index(self._closest_interval) + 2
    
    def draw_slider(self):
        playernum = self.calc_slider()
        pygame.draw.line(self._screen, (self._slider_line_colour), (self._slider_x, self._slider_y), (self._slider_x + self._slider_line_length, self._slider_y), 5)
        pygame.draw.rect(self._screen, self._slider_colour, pygame.Rect(self._slider_mech_x - (self._slider_width / 2), self._slider_y - (self._slider_height/2), self._slider_width,self._slider_height))
        return playernum

class PopUpText():
    def __init__(self, screen, text):
        self._screen = screen
        self._text = text

        self._font = pygame.font.Font(None, 30)
        self._visible = False
        self._done = False

        self._bb_width = 120
        self._bb_height = 120
        self._bb_colour = (196,173,126)
        self._bb_outline = (98,70,34)

        self._lb_width = int(self._bb_width * 0.75)
        self._lb_height = int(self._bb_height * 0.4)
        self._lb_colour = (240, 240, 240)

        self._pos_x = 0
        self._pos_y = 0

        self._player_text = ""

    def open(self):
        if self._visible:
            return

        self._visible = True
        self._done = False
        self._player_text = ""
        self._pos_x, self._pos_y = pygame.mouse.get_pos()

    def close(self):
        self._visible = False
        self._done = True

    def handle_events(self, events):
        if not self._visible:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self._player_text = self._player_text[:-1]

                elif event.key == pygame.K_RETURN:
                    self.close()

                elif event.unicode.isdigit() and len(self._player_text) < 2:
                    self._player_text += event.unicode

    def get_number(self):
        return self._player_text
    
    def reset(self):
        self._visible = False
        self._done = False
        self._player_text = ""

    def get_completed(self):
        return self._done

    def draw(self):
        if not self._visible:
            return

        pygame.draw.rect(self._screen,self._bb_colour,(self._pos_x, self._pos_y, self._bb_width, self._bb_height))
        pygame.draw.rect(self._screen,self._bb_outline,(self._pos_x, self._pos_y, self._bb_width, self._bb_height),5)

        text_surface = self._font.render(self._text, True, (0, 0, 0))
        self._screen.blit(text_surface, (self._pos_x + 5, self._pos_y + 5))

        pygame.draw.rect(self._screen,self._lb_colour,(self._pos_x + 10,self._pos_y + 40,self._lb_width,self._lb_height))

        input_surface = self._font.render(self._player_text, True, (0, 0, 0))
        self._screen.blit(input_surface,(self._pos_x + 15, self._pos_y + 45))

class Userinterface():
    def __init__(self,all_countries,adjacency_list):
        self._printed = True
        self._screen_width = WIDTH
        self._screen_height = HEIGHT
        self._screen = pygame.display.set_mode((self._screen_width,self._screen_height))
        self._state = "mainmenu"
        pygame.font.init()
        self._big_white_font = pygame.font.Font(None,200)
        self._big_red_font = pygame.font.Font(None,193)
        self._base_font = pygame.font.Font(None,45)
        self._error_font = pygame.font.Font(None,30)
        self._newgame_text = ""
        self._newgame_title = ""
        self._countries_organised = False
        self._country_array = []
        self._mouse_position = (0,0)
        self._clicked_country = None
        self._created = False
        self._playernum = 3
        self._playerarr = []
        self._all_countries = all_countries
        self._events = None
        self._completed = False
        self._game = None
        self._load_game_name = None

        self._slider = Slider(self._screen)

        self._got_files = False

        self._files_array = []
        self._files_name_array = []

        self._player_num = 0
        self._phase = "reinforce"
        
        self._heading = ""
        self._subheading = ""

        self._end_text = ""
        self._game_over = False

        self._popup = PopUpText(self._screen,"Number")

        self._overlay = pygame.Surface((self._screen_width, self._screen_height), pygame.SRCALPHA)
        self._dark_rect = pygame.Rect(0, 0, self._screen_width, self._screen_height)

        screen = self._screen

        self._loadgametitle_img = pygame.image.load(DIRPATH+'/UI/loadgame.png').convert_alpha()
        self._gameselect_img = pygame.image.load(DIRPATH+'/UI/GameSelect.png').convert_alpha()
        self._loadgame_img = pygame.image.load(DIRPATH+'/UI/loadgamebutton.png').convert_alpha()
        self._mainmenu_img = pygame.image.load(DIRPATH+'/UI/mainmenubutton.png').convert_alpha()
        self._newgametitle_img = pygame.image.load(DIRPATH+'/UI/newgame.png').convert_alpha()
        self._newgame_img = pygame.image.load(DIRPATH+'/UI/newgamebutton.png').convert_alpha()
        self._quitgame_img = pygame.image.load(DIRPATH+'/UI/quitgamebutton.png').convert_alpha()
        self._startgame_img = pygame.image.load(DIRPATH+'/UI/startgamebutton.png').convert_alpha()
        self._skipphase_img = pygame.image.load(DIRPATH+'/UI/skipphasebutton.png').convert_alpha()
        self._title_img = pygame.image.load(DIRPATH+'/UI/Title.png').convert_alpha()
        self._gamefile_img = pygame.image.load(DIRPATH+'/UI/GameFile.png').convert_alpha()

        self._shallowwater_img = pygame.image.load(DIRPATH+'/UI/ShallowBrown.png').convert_alpha()
        self._countrynames = pygame.image.load(DIRPATH+'/UI/CountryNames.png').convert_alpha()
        self._countryconnections = pygame.image.load(DIRPATH+'/UI/CountryConnections.png').convert_alpha()
        

        self._title_scale = 2
        self._scale = 2

        self._adjacency_list = adjacency_list

        self._mainmenu_button = Button(screen, ((self._screen_width/2) - (int((self._quitgame_img.get_width()*self._scale)/2))), 650, self._mainmenu_img, self._scale)

        self._mainmenu_button_ingame = Button(screen, WIDTH - (self._mainmenu_img.get_width()*self._scale), 0, self._mainmenu_img, self._scale)

        self._newgame_button = Button(screen, ((self._screen_width/2) - (int((self._newgame_img.get_width()*self._scale)/2))), 200, self._newgame_img, self._scale)

        self._loadgame_button = Button(screen, ((self._screen_width/2) - (int((self._loadgame_img.get_width()*self._scale)/2))), 350, self._loadgame_img, self._scale)

        self._quitgame_button = Button(screen, ((self._screen_width/2) - (int((self._quitgame_img.get_width()*self._scale)/2))), 500, self._quitgame_img, self._scale)

        self._startgame_button = Button(screen, ((self._screen_width/2) - (int((self._loadgame_img.get_width()*self._scale)/2))), 500, self._startgame_img, self._scale)

        self._skipphase_button = Button(screen, WIDTH - (self._mainmenu_img.get_width()*self._scale), ((self._skipphase_img.get_height()*self._scale) + 10), self._skipphase_img, self._scale)

        self._title_width = self._title_img.get_width()
        self._title_height = self._title_img.get_height()
        self._title_img = pygame.transform.scale(self._title_img,(int(self._title_width*self._title_scale),(int(self._title_height*self._title_scale))))

    def inputs(self):
        self._events = pygame.event.get()
        for event in self._events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self._state == "hostgame" or self._state == "joingame" or self._state == "lobby":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self._newgame_text = self._newgame_text[:-1]
                        elif len(self._newgame_text) < 21 and event.key != pygame.K_RETURN:
                            self._newgame_text += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._mouse_position = event.pos
                    for country in reversed(self._country_array):
                        country.update_mouse_pos(self._mouse_position)
                        if country.check_clicked():
                            self._clicked_country = country

    def menu_loop(self):
        while True:
            self._screen.fill((190,190,190))

            self.inputs()

            if self._state == "mainmenu":
                self._screen.blit(self._title_img, (int(self._screen_width/2) - (int(self._title_img.get_width()/2)), 35))
                if self._newgame_button.draw() == True:
                    self._state = "hostgame"
                elif self._loadgame_button.draw() == True:
                    self._state = "loadgame"
                elif self._quitgame_button.draw() == True:
                    self._state = "quitgame"
          

            if self._state == "hostgame":
                self.draw_hostgame()
            elif self._state == "loadgame":
                self.draw_loadgame()
            elif self._state == "ingame":
                return self._playernum, self._newgame_text, None
            elif self._state == "lgame":
                return 0, None, self._load_game_name
            elif self._state == "quitgame":
                sys.exit()
            
            fps = CLOCK.get_fps()
            #print(int(fps))
            CLOCK.tick(60)
            
            pygame.display.update()

    def draw_hostgame(self):
        self._screen.blit(self._title_img, (int(self._screen_width/2) - (int(self._title_img.get_width()/2)), 35))
        self._screen.blit(self._newgametitle_img, (int(self._screen_width/2) - (int(self._newgametitle_img.get_width()/2)), 200))

        textbox_width = 500
        textbox_height = 50
        pygame.draw.rect(self._screen, (0, 0, 0), pygame.Rect(((self._screen_width/2) - textbox_width/2), 290, textbox_width, textbox_height), 5)

        TooLongText = "Name must be 20 characters or less"
        NameTooLongSurface = self._error_font.render(TooLongText,True,(0,0,0))
        if len(self._newgame_text) > 20:
            x = self._screen_width // 2 - NameTooLongSurface.get_width() // 2
            self._screen.blit(NameTooLongSurface, (x, 350))

        name_taken = False
        for filename in os.listdir(DIRPATH):
            if f"{self._newgame_text}.json" == filename:
                NameAlreadyTaken = "Name must not be one of your past saves"
                NameAlreadyTakenSurface = self._error_font.render(NameAlreadyTaken,True,(0,0,0))
                x = self._screen_width // 2 - NameTooLongSurface.get_width() // 2
                self._screen.blit(NameAlreadyTakenSurface, (x, 370))
                name_taken = True

        self._playernum = self._slider.draw_slider()
        playernum_text = str(self._playernum)
        playernum_text = f"play a {playernum_text} player game"
        if self._playernum == 2:
            playernum_text = f"play a {playernum_text} player game (not including neutral countries)"
        playernum_surface = self._base_font.render(playernum_text,True,(0,0,0))
        x = (self._screen_width // 2) - (playernum_surface.get_width() // 2)
        self._screen.blit(playernum_surface, (x,470))

        self.newgame_text_surface = self._base_font.render(self._newgame_text,True,(0,0,0))
        self._screen.blit(self.newgame_text_surface,(((self._screen_width/2) - (textbox_width/2) + 5),300))

        if self._startgame_button.draw() == True and name_taken == False:
                self._state = "ingame"
                self._newgame_title = self._newgame_text
                return
        elif self._mainmenu_button.draw() == True:
                self._state = "mainmenu"
                self._newgame_text = ""
                return
        
    def initialise_game_files(self):
        game_files_array = []
        game_files_names_array = []
        index = 5
        for filename in os.listdir(DIRPATH):
            if filename.endswith(".json"):
                file_button_name = filename.removesuffix(".json")
                file_button = Button(self._screen, ((self._screen_width/2) - (int((self._gamefile_img.get_width()*self._scale)/2))), (index * 60), self._gamefile_img, self._scale)
                game_files_array.append(file_button)
                game_files_names_array.append(file_button_name)
                index += 1
        return game_files_array, game_files_names_array
    
    def draw_loadgame(self):
        self._screen.blit(self._title_img, (int(self._screen_width/2) - (int(self._title_img.get_width()/2)), 35))
        self._screen.blit(self._gameselect_img, (int(self._screen_width/2) - (int(self._gameselect_img.get_width()/2)), 200))

        if self._got_files == False:
            self._files_array, self._files_name_array = self.initialise_game_files()
            self._got_files = True

        if len(self._files_array) > 0:
            for i, file in enumerate(self._files_array):
                if file.draw():
                    self._load_game_name = self._files_name_array[i]
                    self._state = "lgame"
                    break

                verticle_offset = 5
                index = (i + verticle_offset) * 60

                GameNameText = self._files_name_array[i]
                GameNameSurface = self._base_font.render(GameNameText,True,(000,000,000))
                x = self._screen_width // 2 - GameNameSurface.get_width() // 2
                self._screen.blit(GameNameSurface, (x, index + 15))

        if self._mainmenu_button.draw() == True:
            self._state = "mainmenu"
            return

    def get_clicked_country_info(self):
        for i in range (len(self._playerarr)):
            if self._clicked_country is not None:
                return self._clicked_country.get_name()
            
    def clear_clicked_country(self):
        self._clicked_country = None

    def finish_attacking(self):
        skipbox_width = 200
        skipbox_height = 150
        pygame.draw.rect(self._screen, (0, 0, 0), pygame.Rect(1600,HEIGHT/2, skipbox_width, skipbox_height), 5)

    def set_completed_True(self):
        self._completed = True

    def set_game_phase(self, phase, player_index, heading, subheading):
        self._phase = phase
        self._player_num = player_index
        self._heading = heading
        self._subheading = subheading

    def set_game(self,game):
        self._game = game

    def set_game_name(self,game_name):
        self._newgame_text = game_name

    def call_save_game(self):
        self._game.save_game(self._playerarr, self._newgame_text, self._heading, self._subheading, self._phase, self._player_num)

    def check_win(self, player):
        if len(player.get_countries()) == 42:
            return True
        else:
            return False

    def draw_game_over(self):
        pygame.draw.rect(self._overlay,(0, 0, 0, 215),self._dark_rect)
        self._screen.blit(self._overlay, (0, 0))

        GameNameSurface = self._big_white_font.render(self._end_text,True,(255,255,255))
        x = self._screen_width // 2 - GameNameSurface.get_width() // 2
        self._screen.blit(GameNameSurface, (x, 300))
        
        GameNameSurface = self._big_red_font.render(self._end_text,True,(255,0,0))
        x = self._screen_width // 2 - GameNameSurface.get_width() // 2
        self._screen.blit(GameNameSurface, (x, 297))

        if self._mainmenu_button.draw() == True:
            self._newgame_text = ""
            return "mainmenu"

    def game_loop(self):
        self._completed = False
        created = False
        player = self._playerarr[self._player_num]

        while True:
                    if player.get_name() == "Neutral":
                        self._player_num = (self._player_num + 1) % self._playernum 
                        player = self._playerarr[self._player_num]
                    self._screen.fill((196,173,126))
                    self._screen.blit(self._shallowwater_img, (70,40))
                    self._screen.blit(self._countryconnections, (00,175))

                    if self._game_over == False:
                        if player.get_countries() == []:
                            self._player_num = (self._player_num + 1) % self._playernum
                            player = self._playerarr[self._player_num]
                        
                        if self._phase == "reinforce":
                            self.call_save_game()
                            if created == False:
                                newReinforce = Reinforce(self._playerarr,player,self._all_countries,self._country_array,self._popup,self, self._adjacency_list)
                                newReinforce.calc_reinforcements()
                                created = True
                            else:
                                if player.is_ai() == False:
                                    ReinforceText = (f"{str(player.get_reinforcements())} reinforcements remaining")
                                    ReinforceSurface = self._error_font.render(ReinforceText,True,(000,000,000))
                                    self._screen.blit(ReinforceSurface, ((WIDTH/2) - (ReinforceSurface.get_width()/2),75))

                                newReinforce.set_clicked_country(self._clicked_country)
                                self._completed = newReinforce.reinforce_assign()
                                if self._completed == True:
                                    if player.is_ai():
                                        time.sleep(1)
                                    self._phase = "attack"
                                    created = False
                                    
                        elif self._phase == "attack":
                            self.call_save_game()
                            if created == False:
                                newAttack = Attack(self._playerarr, player, self._all_countries, self._country_array, self._popup, self, self._adjacency_list)
                                created = True
                                self._completed = False
                            else:
                                if self.check_win(player):
                                    if player.is_ai():
                                        self._end_text = "YOU LOST"
                                    else:
                                        self._end_text = "YOU WON"
                                    self._game_over = True
                                    continue
                                if player.is_ai() == False:
                                    if self._skipphase_button.draw() == True:
                                        self._completed = True
                                        newAttack.invalid_turn()
                                if self._completed == False:
                                    if newAttack.get_countries():
                                        self._completed = True
                                if self._completed == True:
                                    if player.is_ai():
                                        time.sleep(1)
                                    self._phase = "fortify"
                                    created = False

                        elif self._phase == "fortify":
                            self.call_save_game()
                            if created == False:
                                newFortify = Fortify(self._playerarr,player,self._all_countries,self._country_array,self._popup,self,self._adjacency_list)
                                created = True
                                self._completed = False
                            else:
                                if player.is_ai() == False:
                                    if self._skipphase_button.draw() == True:
                                        self._completed = True
                                        newFortify.invalid_turn()
                                if self._completed == False:
                                    if newFortify.get_countries():
                                        self._completed = True
                                if self._completed == True:
                                    if player.is_ai():
                                        time.sleep(1)
                                    self._phase = "reinforce"
                                    created = False
                                    self._player_num = (self._player_num + 1) % self._playernum
                                    player = self._playerarr[self._player_num]

                    self._screen.blit(self._title_img, (0, 0))

                    heading_surface = self._base_font.render(self._heading,True,(0,0,0))
                    subheading_surface = self._base_font.render(self._subheading,True,(0,0,0))

                    x_pos_h = self._screen_width // 2 - heading_surface.get_width() // 2
                    self._screen.blit(heading_surface, (x_pos_h, 10))

                    x_pos_sh = self._screen_width // 2 - subheading_surface.get_width() // 2
                    self._screen.blit(subheading_surface, (x_pos_sh, 40))

                    index = 10
                    pygame.draw.rect(self._screen,(0,0,0),((WIDTH - 200) -15 , (index * 50) - 15, 185, len(self._playerarr * 50) + 15,),3)
                    for p in self._playerarr:
                        player_text = p.get_name()
                        player_text_surface = self._base_font.render(player_text,True,(0,0,0))
                        self._screen.blit(player_text_surface, (WIDTH - 200, index * 50))

                        pygame.draw.rect(self._screen,p.get_colour(),((WIDTH - 200) + 120 , index * 50, 30, 30))
                        pygame.draw.rect(self._screen,(0,0,0),((WIDTH - 200) + 120 , index * 50, 30, 30,),2)
                        index += 1

                    self.inputs()
                    self._popup.handle_events(self._events)
                    self.draw_countries()
                    self.get_clicked_country_info()
                    self._screen.blit(self._countrynames, (150,130))
                    self._popup.draw()

                    if self._mainmenu_button_ingame.draw() == True:
                        return

                    if self._game_over:
                        if self.draw_game_over() == "mainmenu":
                            return

                    fps = CLOCK.get_fps()
                    #print(int(fps))
                    CLOCK.tick(60)
                    pygame.display.update()

    def draw_countries(self):
        if self._countries_organised == False:
            for country_name, (directory, location) in self._all_countries.items():
                self._country_array.append(Country_Class(country_name,directory,location,self._playerarr,self._mouse_position))
            self._countries_organised = True

        for c in self._country_array:
            c.draw_country(self._screen)

    def set_playerarr(self,playerarr):
        self._playerarr = playerarr

    def set_heading(self,heading):
        self._heading = heading

    def set_subheading(self,subheading):
        self._subheading = subheading
