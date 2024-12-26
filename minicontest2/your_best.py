# myTeam.py
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


from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
 
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)
    self.team = CaptureAgent.getTeam(self, gameState)
    self.oppon = CaptureAgent.getOpponents(self, gameState)
    self.score = CaptureAgent.getScore(self, gameState)
    self.offFood = CaptureAgent.getFood(self, gameState)
    self.defFood = CaptureAgent.getFoodYouAreDefending(self, gameState)

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    values = [self.evaluate(gameState, a) for a in actions]

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(self.offFood.asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}
  
  def getNearestGhost(self, gameState):
    enemies = [gameState.getAgentState(i) for i in self.oppon]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    pos = gameState.getAgentState(self.index).getPosition()
    if len(ghosts) > 0:
      minDistance = min([self.getMazeDistance(pos, ghost.getPosition()) for ghost in ghosts])
      return minDistance
    else:
      return 9999
    
  def getNearestPac(self, gameState):
    enemies = [gameState.getAgentState(i) for i in self.oppon]
    pacs = [a for a in enemies if a.isPacman and a.getPosition() != None]
    pos = gameState.getAgentState(self.index).getPosition()
    if len(pacs) > 0:
      minDistance = min([self.getMazeDistance(pos, pac.getPosition()) for pac in pacs])
      return minDistance
    else:
      return 9999
  
  def getNearestPacAndPos(self, gameState):
    enemies = [gameState.getAgentState(i) for i in self.oppon]
    pacs = [a for a in enemies if a.isPacman and a.getPosition() != None]
    pos = gameState.getAgentState(self.index).getPosition()
    if len(pacs) > 0:
      pacList = [(pac.getPosition(), self.getMazeDistance(pos, pac.getPosition())) for pac in pacs]
      pacPos, pacDist = zip(*pacList)
      minPacDist = min(pacDist)
      return (minPacDist, pacPos[pacDist.index(minPacDist)])
    else:
      return (9999, None)
    
  def isNotSafe(self, gameState):
    enemies = [gameState.getAgentState(i) for i in self.oppon]
    safe = [a for a in enemies if a.scaredTimer > 3]
    return not safe

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    # successor score same as baseline
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    capList = self.getCapsules(successor)
    features['successorScore'] = -len(foodList)#self.getScore(successor)

    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      # distance to food : nearest one is prefered
      curPos = gameState.getAgentState(self.index).getPosition()
      Pos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(Pos, food) for food in foodList])
      features['distanceToFood'] = minDistance

      # distance to near ghost : farthest one is prefered
      minGhost = self.getNearestGhost(successor)
      if minGhost < 3 and self.isNotSafe(successor):
        features['distanceToNearGhost'] = minGhost
      else:
        features['distanceToNearGhost'] = 0

      # distance to near pac : if small enough, chase opponent's pacman
      #features['stop'] = 0
      #features['reverse'] = 0
      (minPac, pacPos) = self.getNearestPacAndPos(successor)
      if minPac < 4:
        curPac = self.getMazeDistance(curPos, pacPos)
        nextPac = self.getMazeDistance(Pos, pacPos)
        features['distanceToNearPac'] = 15 ** (1/(minPac + 1) + (curPac-nextPac))
        #if action == Directions.STOP: 
        #  features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        #if action == rev: 
        #  features['reverse'] = 1
      else:
        features['distanceToNearPac'] = 0

      # carrying foods : if carrying enough, go to the base
      carry = gameState.getAgentState(self.index).numCarrying
      if (carry == 1 and self.score <= 0) or (carry >= 3):
        curDistance = self.getMazeDistance(curPos, self.start)
        nextDistance = self.getMazeDistance(Pos, self.start)
        features['baseBonus'] = 15 ** ((1/(nextDistance + 1)) + (curDistance-nextDistance))
      else:
        features['baseBonus'] = 0

      # distance to near power capsules : if small enough eat power capsule
      if capList:
        minCap = min([self.getMazeDistance(Pos, cap) for cap in capList])
        if minGhost < 5:
          features['capsuleBonus'] = minCap
          features['baseBonus'] = 0
        else:
          features['capsuleBonus'] = 0
      else:
        features['capsuleBonus'] = 0

    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1, 'distanceToNearGhost': -10, 'distanceToNearPac': 1, 'baseBonus': 1, 'capsuleBonus': 1}

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    # distance to near opponent's ghost : if no invaders, nearest one is prefered
    minGhost = self.getNearestGhost(successor)
    if len(invaders) == 0:
      features['distanceToNearGhost'] = minGhost
    else:
      features['distanceToNearGhost'] = 0


    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'distanceToNearGhost': -1, 'stop': -100, 'reverse': -2}
  