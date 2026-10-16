import random
import time

class Player():
    def __init__(self, name, colour, countries, armies, reinforcements):
        self._name = name
        self._colour = colour
        self._countries = countries
        self._armies = armies
        self._reinforcements = reinforcements

    def set_reinforcements(self, reinforcements):
        self._reinforcements = reinforcements

    def is_ai(self):
        return False
    
    def get_name(self):
        return self._name
    
    def get_colour(self):
        return self._colour
    
    def get_countries(self):
        return self._countries

    def get_armies(self):
        return self._armies
    
    def get_reinforcements(self):
        return self._reinforcements
    
    def set_reinforcements(self, reinforcements):
        self._reinforcements = reinforcements

    def __str__(self):
        return f"name: {self.name}, colour: {self.colour}, countries: {self._countries}, armies: {self._armies}, reinforcements: {self._reinforcements}"

class AI_Player(Player):
    def __init__(self,name, colour, countries, armies, reinforcements):
        super().__init__(name, colour, countries, armies, reinforcements)
        self.__sample_size = 500
        self.__poss_att_countries = self._countries.copy()
        self.__threshold = 40

    def is_ai(self):
        return True

    def get_country_object(self,countryarr,country):
        for c in countryarr:
            if c.get_name() == country:
                return c

    def choose_reinforce_country(self, countryarr, adjacency_list):
        if len(self._countries) == 1:   #if theres only one country then reinforce it
            for c in countryarr:
                if c.get_name() == self._countries[0]:
                    return c
        eb = [] #initialise arrays for counting countries (parallel arrays)
        fb = []
        c = []
        for country in countryarr:  #array of country objects
            if country.get_name() in self._countries:
                enemy_borders = 0   #initialise vars for counting countries
                friendly_borders = 0
                for neighbour in adjacency_list[country.get_name()]:
                    if neighbour in self._countries:
                        friendly_borders += 1   #count enemy and friendly connections
                    else:
                        enemy_borders += 1

                eb.append(enemy_borders)    #add the connections to the parallel arrays
                fb.append(friendly_borders)
                c.append(country)   #add what country it is

        armies = [] 
        for country in c:   
            armies.append(country.get_armies())
        max_armies = max(armies)    #get the max amount of armies owned on one country


        best_index = None   #initialise vars for keeping scores of which countries to reinforce
        best_score = -9999999

        for i in range(len(c)):
            if c[i].get_armies() == max_armies:     #skip strongest country
                continue

            #calculations to find most vulnerable country
            friendly_penalty = abs(fb[i] - 1)   #penalise the amount of friendly countries (more/less) next to the country, so that 1 bordering country is the best
            army_penalty = c[i].get_armies() * 2    #the bigger the army on the country, the bigger the penalty, meaning it reinforces weak countries
            score = (eb[i] * 10) - (friendly_penalty * 5) - army_penalty    #calculate the final score
            if best_index is None or score > best_score:    #find the best score
                best_score = score
                best_index = i

        if best_index is None:  #if there isnt an ideal country to reinforce, reinforce the first one in the array of countries
            return c[0]

        return c[best_index]    #return the best score
 
    def choose_reinforce_armies(self):
        if self._reinforcements > 0:
            reinforce_num = random.randint(1,self._reinforcements)
            return reinforce_num
        return 0

    def choose_attack_countries(self, adjacency_list, countryarr, attacking):
        if len(self._countries) == 1:   #if there's only 1 country then it should attack from that country
            att_c = self._countries[0]
            for country in adjacency_list[att_c]:
                if country not in self._countries:
                    def_c = country
            return att_c, def_c

        probabilities = []  #initialise parallel arrays
        attacking_countries = []
        defending_countries = []

        att_armies = 0  #initialise vars to calculate the attacks
        def_armies = 0
        att_country = None
        def_country = None
        for Acountry in countryarr: #loops through countries and selects the ones owned by the AI
            if Acountry.get_name() in self._countries:
                if Acountry.get_armies() > 1:   #if theres enough armies to attack with
                    att_country = Acountry.get_name()   #store the relevant data
                    att_armies = Acountry.get_armies()
                    for Dcountry in countryarr: #loops through countries and selects ones not owned by the AI
                        if Dcountry.get_name() not in self._countries:
                            if Dcountry.get_name() in adjacency_list[att_country]:  #if it borders the country owned by the AI
                                def_country = Dcountry.get_name()   #stores the relevant data
                                def_armies = Dcountry.get_armies()

                                wins = 0    #initialise the win counter
                                for sample in range(self.__sample_size):    #loops the amount of times specified by sample size
                                    if att_armies >= 3: #get the relevant number of dice to roll for the attacker (AI)
                                        att_dice = att_armies - random.randint(1,2)
                                        if att_dice > 3:
                                            att_dice = 3
                                        def_dice = def_armies
                                        if def_dice > 2:    #gets number of dice to rroll for defender
                                            def_dice = 2
                                        
                                        att_results = []    #initialise attacking and defending arrays
                                        def_results = []

                                        for dice in range(att_dice):
                                            result = random.randint(1,6)
                                            att_results.append(result)  #add results to the arrays
                                        att_results = sorted(att_results, reverse = True)   #organise the results from highest to lowest
                                        for dice in range(def_dice):    #repeat for the defender
                                            result = random.randint(1,6)
                                            def_results.append(result)
                                        def_results = sorted(def_results, reverse = True)

                                        att_points = 0  #initialise points vars for the sum
                                        def_points = 0
                                        for ar, dr in zip(att_results,def_results):     #loop through the organised results and count who won according to the risk dice rules
                                            if ar > dr:
                                                att_points += 1
                                            else:
                                                def_points += 1

                                        if att_points > def_points: #a win is added to the win counter if attacker won
                                            wins += 1

                                victory_prob = (wins / self.__sample_size) * 100    #if the probability of victory is above the threshold then it will attack
                                if victory_prob > self.__threshold:
                                    probabilities.append(victory_prob)  #append the data to the parallel arrays
                                    attacking_countries.append(att_country)
                                    defending_countries.append(def_country)

        if len(defending_countries) == 1:   #if theres only 1 defending left country then lower the threshold to 10 due to imminant victory
            self.__threshold = 10
        if not probabilities:   #if the parallel arrays for countries to attack are empty then attack phase should be skipped
            attacking.done_attacking()
        prob = 0
        att_c = None
        def_c = None
        for i in range(len(probabilities)):
            if probabilities[i] == max(probabilities):  #get the highest probability of winning battle
                prob = probabilities[i]
                att_c = attacking_countries[i]
                def_c = defending_countries[i]
        return att_c,def_c      #return the attacking and defending countries

    def choose_attack_num(self, countryarr, attacking_country):
        if len(self._countries) == 1:
            for country in countryarr:
                if country.get_name() == attacking_country:
                    if country.get_armies() < 2:
                        return None
                    else:
                        attack_num = country.get_armies() - 1
                        if attack_num > 3:
                            attack_num = 3
                            return attack_num
        attack_num = 0
        for country in countryarr:
            if country.get_name() == attacking_country:
                if country.get_armies() > 3:
                    attack_num = random.choice([1,1,2])
                elif country.get_armies() == 3:
                    attack_num = 2
                else:
                    attack_num = 1
        if attack_num != 0:
            return attack_num
        else:
            return attack_num

    def fortify_operations(self, adjacency_list, countryarr, playerarr):
        if len(countryarr) < 3:
            return True     #if there isnt enough countries to complete a fortification then return true to skip the phase
        move_from, armies = self.choose_fortify_from(adjacency_list,countryarr) #AI choice for from country
        if move_from != None:
            enemy, path = self.choose_fortify_to(adjacency_list,countryarr,move_from.get_name())    #ai chpice for to country
            if enemy != None and path != None:  #if there's something in both enemy and path
                for c in countryarr:
                    if c.get_name() == path[1]: #do the operations to update the data and the screen
                        c.set_armies(armies)
                        self._armies[self._countries.index(path[1])] += armies
                        c.update_country(playerarr)
                    if c.get_name() == move_from.get_name():
                        c.set_armies(1)
                        self._armies[self._countries.index(move_from.get_name())] = 1
                        c.update_country(playerarr)
                time.sleep(1.5)
                return True    #return True for a completed fortify
            else:
                time.sleep(1.5)
                return True #skip fortify if theres None in enemy or path
        else:
            time.sleep(1.5)
            return True #skip if there wa snever a move from location
                        
    def choose_fortify_to(self, adjacency_list, countryarr, move_from):
        queue = [move_from]     #create a queue to store the next countries to visit
        visited = set([move_from])  #store the visited countries (with the root)
        parents = {}    #a dictionary containing the parents to each country

        while queue:    #while the queue isnt empty
            current = queue.pop(0)  #remove the first item from the queue and assign it to current

            for neighbor in adjacency_list[current]:    #loop through adjacency list
                if neighbor not in visited: #if the neighbour isnt visited then add it to visited, and add it to parents dict alongside current
                    visited.add(neighbor)   #add to visited
                    parents[neighbor] = current
                    queue.append(neighbor)  #add the neighbour to the end of the queue
                    if neighbor not in self._countries:
                        path = [neighbor]   #track the path
                        back = current  #store current again
                        while back != move_from:    #if back isnt the move from, append it to the path and add it to the parents dict
                            path.append(back)
                            back = parents[back]
                        path.append(move_from)  #add the move from to the end of the path and reverse it to get the right order
                        path.reverse()
                        return neighbor, path   #return the neighbout and path
        return None, None   #return None, None if there isnt an available fortify
                                                                                
    def choose_fortify_from(self, adjacency_list, countryarr):
        from_country = None
        best_surplus = 0    #initialise vars to count where most troops are
        
        armies = None

        for ca in countryarr:
            if ca.get_name() in self._countries:    #get countries owned by the AI
                enemies = 0
                for enemy in adjacency_list[ca.get_name()]: #count the number of enemies it borders
                    if enemy not in self._countries:
                        enemies += 1

                if enemies == 0:    #if it borders 0 enemies then find the surplus. if not then it will iterate again
                    my_armies = ca.get_armies() 
                    surplus = my_armies - 1
                    
                    if surplus > best_surplus:  #find whichever country has the best surplus of armies
                        best_surplus = surplus
                        from_country = ca
                        armies = ca.get_armies() - 1

        return from_country, armies #return the from country and amount or None, None
