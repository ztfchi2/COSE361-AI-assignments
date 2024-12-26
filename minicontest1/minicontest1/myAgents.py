# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from game import Agent, Directions
from searchProblems import PositionSearchProblem
from itertools import combinations

import util
import time
import search
import sys
import math
import random

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
pac_num = 0
once = 1
moving_agent = None
direction_list = [Directions.NORTH, Directions.EAST, Directions.SOUTH, Directions.WEST]

def createAgents(num_pacmen, agent='MyAgent'):
    global pac_num
    pac_num = num_pacmen
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    def limits(self, x, state):
        partitions = math.ceil(state.getFood().width/pac_num)
        eps = partitions * 0.1
        lower_limit = self.index*partitions - eps
        upper_limit = (self.index+1)*partitions + eps
        return x >= lower_limit and x <= upper_limit
    
    def limited_BFS(self, problem, state):
        pacmanInitial = [state.getPacmanPosition(self.index), [], 0]
        visitedPosition = set()
        # visitedPosition.add(problem.getStartState())
        fringe = util.PriorityQueue()
        fringe.push(pacmanInitial, pacmanInitial[2])
        while fringe.isEmpty() == False:
            pacmanCurrent = fringe.pop()
            if pacmanCurrent[0] in visitedPosition:
                continue
            else:
                visitedPosition.add(pacmanCurrent[0])
            if problem.isGoalState(pacmanCurrent[0]) and self.limits(pacmanCurrent[0][0], state):
                return pacmanCurrent[1]
            elif problem.isGoalState(pacmanCurrent[0]) and self.index == moving_agent and self.allCollect == True:
                return pacmanCurrent[1]
            else:
                pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
            Successor = []
            for item in pacmanSuccessors:  # item: [(x,y), 'direction', cost]
                if item[0] not in visitedPosition:
                    pacmanRoute = pacmanCurrent[1].copy()
                    pacmanRoute.append(item[1])
                    sumCost = pacmanCurrent[2]
                    Successor.append([item[0], pacmanRoute, sumCost + item[2]])
            for item in Successor:
                fringe.push(item, item[2])
        return None
    
    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        global once
        global moving_agent
        if once == 1:
            pac_num_list = list(range(pac_num))
            pac_comb = list(combinations(pac_num_list, 2))            

            # Generate list of moving agent candidates
            # adjacent pacmen are added multiple times, increasing their probability of selection
            adj_pac = pac_num_list.copy()    # at least one agent is in this list
            far_agent = None
            for comb in pac_comb:
                a, b = comb
                a_pos = state.getPacmanPosition(a)
                b_pos = state.getPacmanPosition(b)

                if (a_pos[0]-7 <= b_pos[0] and b_pos[0] <= a_pos[0]+7) \
                    and (a_pos[1]-7 <= b_pos[1] and b_pos[1] <= a_pos[1]+7):
                    adj_pac.extend(comb)
        
            # Select one as keep moving agent
            moving_agent = random.choice(adj_pac)
            once = 0
        
        # rest
        if self.allCollect == True and self.index != moving_agent:
            return Directions.STOP
        
        if self.actions.isEmpty() == False:
            # keep following nearest food path
            return self.actions.pop()
        else:
            # find new food path
            problem = AnyFoodSearchProblem(state, self.index) 
            route = self.limited_BFS(problem,state)
            if route != None:
                # all food eating finished
                for step in route:
                    self.actions.push(step)
                return self.actions.pop()
            else:
                # start resting
                self.allCollect = True
                return Directions.STOP

        #return 0
        raise NotImplementedError()

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE ***"
        self.allCollect=False
        self.actions=util.Queue()
        return 0

        raise NotImplementedError()


def NearestFood(Startstate, food_list):
    food_dis = sys.maxsize
    nearest_food = None
    for food in food_list:
        temp = util.manhattanDistance(Startstate, food)
        if food_dis > temp:
            food_dis = temp
            nearest_food = food
    return nearest_food
    
def FarthestFood(Startstate, food_list):
    food_dis = ~sys.maxsize
    farthest_food = None
    for food in food_list:
        temp = util.manhattanDistance(Startstate, food)
        if food_dis < temp:
            food_dis = temp
            farthest_food = temp
    return farthest_food

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"
        pacmanCurrent = [problem.getStartState(), [], 0]
        visitedPosition = set()
        # visitedPosition.add(problem.getStartState())
        fringe = util.PriorityQueue()
        fringe.push(pacmanCurrent, pacmanCurrent[2])
        while not fringe.isEmpty():
            pacmanCurrent = fringe.pop()
            if pacmanCurrent[0] in visitedPosition:
                continue
            else:
                visitedPosition.add(pacmanCurrent[0])
            if problem.isGoalState(pacmanCurrent[0]):
                return pacmanCurrent[1]
            else:
                pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
            Successor = []
            for item in pacmanSuccessors:  # item: [(x,y), 'direction', cost]
                if item[0] not in visitedPosition:
                    pacmanRoute = pacmanCurrent[1].copy()
                    pacmanRoute.append(item[1])
                    sumCost = pacmanCurrent[2]
                    Successor.append([item[0], pacmanRoute, sumCost + item[2]])
            for item in Successor:
                fringe.push(item, item[2])
        return pacmanCurrent[1]

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex, goal=(10,10)):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self.goal = goal
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        if self.food[x][y] == True:
            return True
        return False

