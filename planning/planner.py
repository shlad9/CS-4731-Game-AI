from constants import *
from utils import *
from core import *

import pdb
import copy
from functools import reduce

from statesactions import *
from queue import PriorityQueue

############################
## HELPERS

### Return true if the given state object is a goal. Goal is a State object too.
def is_goal(state, goal):
  return len(goal.propositions.difference(state.propositions)) == 0

### Return true if the given state is in a set of states.
def state_in_set(state, set_of_states):
  for s in set_of_states:
    if s.propositions == state.propositions:
      return True
  return False

### For debugging, print each state in a list of states
def print_states(states):
  for s in states:
    ca = None
    if s.causing_action is not None:
      ca = s.causing_action.name
    print(s.id, s.propositions, ca, s.get_g(), s.get_h(), s.get_f())

def less_than(self, other):
  return self.get_f() < other.get_f()
State.__lt__ = less_than

############################
### Planner 
###
### The planner knows how to generate a plan using a-star and heuristic search planning.
### It also knows how to execute plans in a continuous, time environment.

class Planner():

  def __init__(self):
    self.running = False              # is the planner running?
    self.world = None                 # pointer back to the world
    self.the_plan = []                # the plan (when generated)
    self.initial_state = None         # Initial state (State object)
    self.goal_state = None            # Goal state (State object)
    self.actions = []                 # list of actions (Action objects)

  ### Start running
  def start(self):
    self.running = True
    
  ### Stop running
  def stop(self):
    self.running = False

  ### Called every tick. Executes the plan if there is one
  def update(self, delta = 0):
    result = False # default return value
    if self.running and len(self.the_plan) > 0:
      # I have a plan, so execute the first action in the plan
      self.the_plan[0].agent = self
      result = self.the_plan[0].execute(delta)
      if result == False:
        # action failed
        print("AGENT FAILED")
        self.the_plan = []
      elif result == True:
        # action succeeded
        done_action = self.the_plan.pop(0)
        print("ACTION", done_action.name, "SUCCEEDED")
        done_action.reset()
    # If the result is None, the action is still executing
    return result

  ### Call back from Action class. Pass through to world
  def check_preconditions(self, preconds):
    if self.world is not None:
      return self.world.check_preconditions(preconds)
    return False

  ### Call back from Action class. Pass through to world
  def get_x_y_for_label(self, label):
    if self.world is not None:
      return self.world.get_x_y_for_label(label)
    return None

  ### Call back from Action class. Pass through to world
  def trigger(self, action):
    if self.world is not None:
      return self.world.trigger(action)
    return False

  ### Generate a plan. Init and goal are State objects. Actions is a list of Action objects
  ### Return the plan and the closed list
  def astar(self, init, goal, actions):
      plan = []    # the final plan
      open = []    # the open list (priority queue) holding State objects
      closed = []  # the closed list (already visited states). Holds state objects
      ### YOUR CODE GOES HERE
      start = init

      open = PriorityQueue()
      open.put((start.get_f(), start))

      while not open.empty():
        current = open.get()[1]

        if is_goal(current, goal):
          break
        if not state_in_set(current, closed):
          closed.append(current)
          for action in actions:
            precond = action.preconditions
            prop = current.propositions
            if all(x in prop for x in precond):
              scs = State((current.propositions | action.add_list) - action.delete_list)
              scs.g = current.get_g() + action.cost
              scs.h = self.compute_heuristic(scs, goal, actions)
              scs.parent = current
              scs.causing_action = action
              open.put((scs.get_f(), scs))


      if is_goal(current, goal):
        yuvanesh = current
        while yuvanesh != init:
          plan.append(yuvanesh.causing_action)
          yuvanesh = yuvanesh.parent

      plan.reverse()


      ### CODE ABOVE
      return plan, closed

  ### Compute the heuristic value of the current state using the HSP technique.
  ### Current_state and goal_state are State objects.
  def compute_heuristic(self, current_state, goal_state, actions):
    actions = copy.deepcopy(actions)  # Make a deep copy just in case
    h = 0                             # heuristic value to return
    ### YOUR CODE BELOW

    graph = {}
    dStart, dEnd = Action("dStart", [], current_state.propositions, [], 0), Action("dEnd", goal_state.propositions, [], [], 0)
    actions.append(dStart)
    actions.append(dEnd)

    for action in actions:
      # graph[action] = customNode(action)
      graph[action] = {"oED" : [], "iED" : [], "action" : action}

    for act in actions:
      for action in actions:
        if act != action:
          concat = act.add_list.intersection(action.preconditions)
          for hiram in concat:
            graph[act]['oED'].append((hiram, action, action.cost))
            # graph[act].oED.append((hiram, action, action.cost))
            graph[action]['iED'].append((hiram, act, act.cost))
            # graph[action].iED.append((hiram, act, act.cost))

    running = [(0, dStart)]
    visitedList = []

    while len(running) > 0:
      markov = running.pop(0)
      mappedValue = markov[0]

      mapped = markov[1]
      if graph[mapped]["action"] == dEnd:
        return mappedValue
      if mapped not in visitedList:
        visitedList.append(mapped)

        storage = graph[mapped]['iED']
        costs = [x[2] for x in storage if x[1] in visitedList]
        costs.append(mappedValue)

        maxC = max(costs)
        mappedValue = maxC

        vSet = set()
        for marker in visitedList:
          vSet |= graph[marker]['action'].preconditions
          vSet |= graph[marker]['action'].add_list
        for edgeX in graph[mapped]['oED']:
          child = edgeX[1]
          cProposition = [x[0] for x in graph[child]['iED']]

          if all(m in vSet for m in cProposition):
            running.append(((mappedValue + graph[mapped]["action"].cost), child))
    ###############################################################################################
    ###############################################################################################
    ###############################################################################################

    ### YOUR CODE ABOVE
    return h

