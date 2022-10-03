from pickle import NONE
from random import Random
from game.game_state import GameState
import game.character_class

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy
from util.utility import chebyshev_distance

class KnightScope(Strategy):
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.KNIGHT

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        curr_x = game_state.player_state_list[my_player_index].position.x
        curr_y = game_state.player_state_list[my_player_index].position.y
        curr_gold = game_state.player_state_list[my_player_index].gold
        move_to = Position(5,5);

        #if low hp retreat

        #move towards center slot, based on spawn
        # if((curr_x == 0) & (curr_y == 0)):
        #     move_to = Position(4, 4)
        # elif((curr_x == 0) & (curr_y == 9)):
        #     move_to = Position(4, 5)
        # elif((curr_x == 9) & (curr_y == 0)):
        #     move_to = Position(5, 4)
        # elif((curr_x == 9) & (curr_y == 9)):
        #     move_to = Position(9, 9)
        
        #based on id
        if(my_player_index == 0):
            #move to spawn if gold == 8
            if(curr_gold >= 8):
                return Position(0,0)
            return Position(4, 4)
        elif(my_player_index == 1):
            if(curr_gold >= 8):
                return Position(9,0)
            return Position(5, 4)
        elif(my_player_index == 2):
            if(curr_gold >= 8):
                return Position(9,9)
            return Position(5, 5)
        elif(my_player_index == 3):
            if(curr_gold >= 8):
                return Position(0,9)
            return Position(4, 5)
        
        
        #if moving to spot makes them die, then move to spot that won't make them die
        

        return Position(5,5)

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        min_attack_dis = 10
        atk_enemy = 0
        possible_fatal_hit = False
        for i in range(len(game_state.player_state_list)):
            if(i != my_player_index):
                enemy = game_state.player_state_list[i]
                myplayer = game_state.player_state_list[my_player_index]
                enemy_pos = enemy.position
                curr_pos = game_state.player_state_list[my_player_index].position
                enemy_health = enemy.health
                enemy_score = enemy.score

                fatal_hit = False
                attack_range = myplayer.stat_set.range
                enemy_dis = chebyshev_distance(enemy_pos, curr_pos)
                curr_atk = myplayer.stat_set.damage
                
                #check that enemy is within the range
                if((enemy_dis <= attack_range)):
                    #check that the hit is fatal
                    if(enemy_health < curr_atk):  
                        fatal_hit = True
                        possible_fatal_hit = True
                        #if hit is fatal, and no previous fatal hits, hit enemy
                        if(possible_fatal_hit == False):
                            min_attack_dis = enemy_dis
                            atk_enemy = i
                            return atk_enemy
                        #if other possible fatal hits, hit closest enemy
                        else:
                            if (enemy_dis <= min_attack_dis):
                                min_attack_dis = enemy_dis
                                atk_enemy = i
                                return atk_enemy
                    #if the hit is not fatal, hit the closest enemy
                    if((enemy_health > curr_atk) & (possible_fatal_hit == False)):
                        if(enemy_dis <= min_attack_dis):
                            min_attack_dis = enemy_dis
                            atk_enemy = i
                            return atk_enemy


              
        return atk_enemy

        #return Random().randint(0, 3)

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        if(game_state.player_state_list[my_player_index].gold >= 8):
            return Item.HUNTER_SCOPE
        else:
            return Item.HUNTER_SCOPE
        

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False