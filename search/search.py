# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    hist = util.Counter()   # counting object that checks whether the node is visited
    path = []               # list that is used to check the increment of path (used for debugging)
    cost = []               # list that is used to check the increment of cost (used for debugging)

    stack = util.Stack()
    stack.push((problem.getStartState(), [], 0))        # push in the start state to the stack

    while not stack.isEmpty():                          # loop until the stack becomes empty
        get_state, get_path, get_cost = stack.pop()
        if problem.isGoalState(get_state):              # end procedure when the goal state is popped out
            return get_path

        if hist[get_state] == 0:                        # check if the node is visited
            hist[get_state] = 1                         # visit node
            if get_path != []:
                path.append(get_path)
            cost.append(get_cost)

            succs = problem.getSuccessors(get_state)    # find path (next node)
            for tup in succs:
                next, action, incr = tup
                stack.push((next, get_path+[action], get_cost+incr))    # push in the nodes to the stack
    return []   # no path to the goal
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    hist = util.Counter()   # counting object that checks whether the node is visited
    path = []               # list that is used to check the increment of path (used for debugging)
    cost = []               # list that is used to check the increment of cost (used for debugging)

    queue = util.Queue()
    queue.push((problem.getStartState(), [], 0))        # push in the start state to the queue

    while not queue.isEmpty():                          # loop until the queue becomes empty
        get_state, get_path, get_cost = queue.pop()
        if problem.isGoalState(get_state):              # end procedure when the goal state is popped out
            return get_path

        if hist[get_state] == 0:                        # check if the node is visited
            hist[get_state] = 1                         # visit node
            if get_path != []:
                path.append(get_path)
            cost.append(get_cost)

            succs = problem.getSuccessors(get_state)    # find path (next node)
            for tup in succs:
                next, action, incr = tup
                queue.push((next, get_path+[action], get_cost+incr))    # push in the nodes to the queue
    return []   # no path to the goal
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    hist = util.Counter()   # counting object that checks whether the node is visited
    path = []               # list that is used to check the increment of path (used for debugging)
    cost = []               # list that is used to check the increment of cost (used for debugging)

    pqueue = util.PriorityQueue()
    pqueue.push((problem.getStartState(), [], 0), 0)    # push in the start state to the min-priority queue

    while not pqueue.isEmpty():                         # loop until the min-priority queue becomes empty
        get_state, get_path, get_cost = pqueue.pop()
        if problem.isGoalState(get_state):              # end procedure when the goal state is popped out
            return get_path

        if hist[get_state] == 0:                        # check if the node is visited
            hist[get_state] = 1                         # visit node
            if get_path != []:
                path.append(get_path)
            cost.append(get_cost)

            succs = problem.getSuccessors(get_state)    # find path (next node)
            for tup in succs:
                next, action, incr = tup
                pqueue.push((next, get_path+[action], get_cost+incr), get_cost+incr)    # push in the nodes to the min-priority queue
    return []   # no path to the goal

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    hist = util.Counter()   # counting object that checks whether the node is visited
    path = []               # list that is used to check the increment of path (used for debugging)
    cost = []               # list that is used to check the increment of cost (used for debugging)

    pqueue = util.PriorityQueue()
    pqueue.push((problem.getStartState(), [], 0), 0)    # push in the start state to the min-priority queue

    while not pqueue.isEmpty():                         # loop until the min-priority queue becomes empty
        get_state, get_path, get_cost = pqueue.pop()
        if problem.isGoalState(get_state):              # end procedure when the goal state is popped out
            return get_path

        if hist[get_state] == 0:                        # check if the node is visited
            hist[get_state] = 1                         # visit node
            if get_path != []:
                path.append(get_path)
            cost.append(get_cost)

            succs = problem.getSuccessors(get_state)    # find path (next node)
            for tup in succs:
                next, action, incr = tup
                pqueue.push((next, get_path+[action], get_cost+incr), get_cost+incr+heuristic(next, problem))    # push in the nodes to the min-priority queue, the heuristic function is used
    return []   # no path to the goal
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
