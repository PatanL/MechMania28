from pickle import FALSE
from random import Random
from game.game_state import GameState
import game.character_class
from typing import List

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy
from util.utility import chebyshev_distance, manhattan_distance

class ArcherShieldStrategy(Strategy):
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.ARCHER

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        start: Position
        center: Position
        if my_player_index == 0:
            start = Position(0,0)
            center = Position(4,4)
        if my_player_index == 1:
            start = Position(9,0)
            center = Position(5,4)
        if my_player_index == 2:
            start = Position(9,9)
            center = Position(5,5)
        if my_player_index == 3:
            start = Position(0,9)
            center = Position(4,5)
        if game_state.turn == 8 or (game_state.player_state_list[my_player_index].position == start and game_state.player_state_list[my_player_index].gold>=8 and game_state.player_state_list[my_player_index].item == Item.NONE):
            return start # return to start
        if game_state.player_state_list[my_player_index].item == Item.SHIELD:
            return center
        center_squares = [Position(4,4), Position(4,5), Position(5,4), Position(5,5)]
        for index in [0,1,2,3]:
            if (index == my_player_index):
                continue
            other = game_state.player_state_list[index]
            p2 = other.position
            if p2 in center_squares or other.stat_set.speed in [manhattan_distance(p2,c) for c in center_squares]:
                if game_state.player_state_list[my_player_index].item == Item.NONE:
                    return Position((center.x + start.x)/2, (center.y + start.y)/2)
        return center

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        player_indices = [0,1,2,3]
        
        enemies_attack_list = [[self.can_attack(j, i, game_state) for i in player_indices] for j in player_indices]
        my_attack_list = enemies_attack_list[my_player_index]
        priority_list = [[]]
        
        #priority_list[0] are all players we can attack
        for i in player_indices:
            if my_attack_list[i] == True:
                priority_list[0].append(i)
        #priority_list[1] are all players we can kill
        priority_list.append([])
        for i in priority_list[0]:
            if self.can_kill([my_player_index], i, game_state):
                priority_list[1].append(i)
        #priority_list[2] are all players that other players can attack that we can also attack
        #priority_list[3] are all players that die when we and another player attack it
        priority_list.append([])
        priority_list.append([])
        for i in priority_list[0]:
            for j in player_indices:
                if enemies_attack_list[j][i] == True:
                    priority_list[2].append(i)
                    if self.can_kill([my_player_index, j], i, game_state):
                        priority_list[3].append(i)
        
        if len(priority_list[0]) == 0:
            return 0 #if we can't attack anyone, return -1
        #can attack someone
        if len(priority_list[1]) == 0: #can't kill someone on our own
            if len(priority_list[2]) == 0: #can't attack someone with another player
                return priority_list[0][0]
            if len(priority_list[3]) == 0: #can attack someone but can't kill anyone
                return priority_list[2][0]
            return priority_list[3][0]
        return priority_list[1][0]
        
        

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        if (game_state.player_state_list[my_player_index].item == Item.NONE and game_state.player_state_list[my_player_index].gold >= 8):
            return Item.SHIELD
        return Item.NONE
    
    def can_attack(self, player_index: int, other_player_index: int, game_state: GameState)->bool:
        range = game_state.player_state_list[player_index].stat_set.range
        p1 = game_state.player_state_list[player_index].position
        p2 = game_state.player_state_list[other_player_index].position
        return (chebyshev_distance(p1,p2) <= range) and (player_index != other_player_index)

    def can_kill(self, player_index_list: List[int], victim_index: int, game_state: GameState)->bool:
        total_damage = 0
        for player_index in player_index_list:
            total_damage = total_damage + game_state.player_state_list[player_index].stat_set.damage
            if not self.can_attack(player_index, victim_index, game_state):
                return False
        return game_state.player_state_list[victim_index].health <= total_damage
    
        
                