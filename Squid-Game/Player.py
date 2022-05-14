import numpy as np
import random
import time
import sys
import os 
from BaseAI import BaseAI
from Grid import Grid
from Utils import *

# TO BE IMPLEMENTED
# 
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None
        self.depth=3
    
    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position 

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def compute_IS(self,grid,player,opponent):
        player_moves=grid.get_neighbors(player, only_available=True)
        oppo_moves=grid.get_neighbors(opponent,only_available=True)
        return len(player_moves)-len(oppo_moves)

    def compute_OCLS(self,grid,player,opponent):
        # player
        cur_player_moves=grid.get_neighbors(player, only_available=True)
        sum_player=len(cur_player_moves)
        for i in range(len(cur_player_moves)):
            sum_player+=len(grid.get_neighbors(cur_player_moves[i], only_available=True))+1
        # opponent
        cur_oppo_moves = grid.get_neighbors(opponent, only_available=True)
        sum_oppo=len(cur_oppo_moves)
        for i in range(len(cur_oppo_moves)):
            sum_oppo+=len(grid.get_neighbors(cur_oppo_moves[i], only_available=True))+1
        return sum_player-sum_oppo

    def compute_h(self,grid,player,opponent):
        return self.compute_OCLS(grid,player,opponent)

    def dfs_move(self,grid, alpha,beta,oppo_pos,level): #oppo_pos is the position of the opponent
        res=-1
        if level == self.depth:
            return self.compute_h(grid, self.pos, oppo_pos)
        elif level%2==1: # max
            # expand max node
            move_cells = grid.get_neighbors(self.pos, only_available=True)
            # chance
            old_pos=self.pos
            for i in range(len(move_cells)):
                self.pos=move_cells[i]
                grid.setCellValue(old_pos,0)
                grid.setCellValue(move_cells[i],self.player_num) # change the grid
                tmp = self.dfs_move(grid, alpha, beta, oppo_pos, level + 1)
                if tmp>=alpha:
                    alpha=tmp
                    if level == 1:
                        res=move_cells[i]
                self.pos=old_pos
                grid.setCellValue(move_cells[i],0)
                grid.setCellValue(old_pos, self.player_num) #recover the grid
                if alpha>=beta: # cut
                    break

        elif level%2==0: #min
            # expand min node
            trap_cells = grid.get_neighbors(self.pos,only_available=True)
            if trap_cells==[]:
                trap_cells = grid.get_neighbors(self.pos)
                trap_cells = [t for t in trap_cells if grid.getCellValue(t) <= 0]
            # chance
            for i in range(len(trap_cells)):
                neighbors = grid.get_neighbors(trap_cells[i])
                neighbors = [neighbor for neighbor in neighbors if grid.getCellValue(neighbor) <= 0]
                n = len(neighbors)

                p = 1 - 0.05 * (manhattan_distance(trap_cells[i], oppo_pos) - 1)

                if p==1:  # the trap is next to the thrower
                    probs = [p]
                    traps = [trap_cells[i]]
                else:
                    probs = np.ones(1 + n)
                    probs[0] = p
                    probs[1:] = np.ones(n) * ((1 - p) / n)
                    traps = [trap_cells[i]] + neighbors

                chance_value = 0
                for j in range(len(traps)):
                    if grid.getCellValue(traps[j])==-1: # is already a trap
                        chance_value += probs[j] * self.dfs_move(grid, alpha, beta, oppo_pos, level + 1)
                    else:
                        grid.trap(traps[j]) # change the grid
                        chance_value += probs[j] * self.dfs_move(grid, alpha, beta, oppo_pos, level + 1)
                        grid.setCellValue(traps[j],0) # recover the grid
                beta = min(beta, chance_value)
                if alpha >= beta:
                    break
        # return
        if level==1:
            return res
        elif level%2==1:
            return alpha
        elif level%2==0:
            return beta

    def dfs_trap(self,grid, alpha,beta,oppo_pos,level): #oppo_pos is the position of the opponent
        res=-1
        if level==self.depth:
            return self.compute_h(grid,self.pos,oppo_pos)
        elif level%2==1: # max
            # expand max node
            trap_cells = grid.get_neighbors(oppo_pos,only_available=True)
            if trap_cells==[]:
                trap_cells = grid.get_neighbors(oppo_pos)
                trap_cells = [t for t in trap_cells if grid.getCellValue(t) <= 0]
            # chance
            for i in range(len(trap_cells)):
                neighbors = grid.get_neighbors(trap_cells[i])
                neighbors = [neighbor for neighbor in neighbors if grid.getCellValue(neighbor) <= 0]
                n = len(neighbors)
                p = 1 - 0.05 * (manhattan_distance(self.pos, trap_cells[i]) - 1)
                if p == 1:  # the trap is next to the thrower
                    probs = [p]
                    traps = [trap_cells[i]]
                else:
                    probs = np.ones(1 + n)
                    probs[0] = p
                    probs[1:] = np.ones(n) * ((1 - p) / n)
                    traps = [trap_cells[i]] + neighbors

                chance_value=0
                for j in range(len(traps)):
                    if grid.getCellValue(traps[j]) == -1:
                        chance_value += probs[j] * self.dfs_trap(grid, alpha, beta, oppo_pos, level + 1)
                    else:
                        grid.trap(traps[j])
                        chance_value+=probs[j]*self.dfs_trap(grid,alpha,beta,oppo_pos,level+1)
                        grid.setCellValue(traps[j], 0)  # recover the grid

                if alpha<=chance_value:
                    alpha = chance_value
                    if level==1:
                        res=trap_cells[i]
                if alpha>=beta:
                    break
        elif level%2==0: # min
            # expand min node
            move_cells = grid.get_neighbors(oppo_pos, only_available=True)
            # update beta
            old_pos=oppo_pos
            for i in range(len(move_cells)):
                grid.setCellValue(old_pos,0)
                grid.setCellValue(move_cells[i], 3-self.player_num)  # change the grid
                beta=min(beta,self.dfs_trap(grid,alpha,beta,move_cells[i],level+1))
                grid.setCellValue(move_cells[i],0)
                grid.setCellValue(old_pos, 3-self.player_num)  # recover the grid
                if alpha>=beta: # cut
                    break
                # return
        if level == 1:
            return res
        elif level%2==1:
            return alpha
        elif level % 2 == 0:
            return beta


    def getMove(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions, 
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        opponent = grid.find(3 - self.player_num)
        alpha = -float('inf')
        beta = float('inf')
        return self.dfs_move(grid, alpha,beta,opponent,1)

    def getTrap(self, grid : Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        # find opponent
        opponent = grid.find(3 - self.player_num)
        alpha=-float('inf')
        beta=float('inf')
        return self.dfs_trap(grid, alpha, beta, opponent, 1)