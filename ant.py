from settings import *
from agent import Agent
from random import uniform

class Ant(Agent):
  FORWARDS  = 0
  BACKWARDS = 1

  def __init__(self, world, location, direction = None):
    super(Ant, self).__init__()

    self.world = world;

    self.direction      = direction or self.FORWARDS
    self.history        = []          # a list of trips
    self.trip           = [location]  # a list of nodes forming a complete cycle
    self.return_trip    = [location]
    self.return_length  = None

  def move(self):
    """Move the ant"""
    #x = self.trip[:]
    self.trip.append(self.choose())

    #print map(reverse_node, x), '->', map(reverse_node, self.trip)
    #print map(reverse_node, self.return_trip)

    # Add the return trip information
    if self.direction == self.FORWARDS:
      self.return_trip.append(self.trip[-1])
      # check for and remove cycles
      index = self.return_trip.index(self.trip[-1])
      if index != len(self.return_trip)-1:
        self.return_trip = self.return_trip[:index+1]

    # Let the observers know there the ant moved (only on the return journey)
    if self.direction == self.BACKWARDS:
      self.notify()

    # If we're headed for the destination (FOOD)
    if self.direction == self.FORWARDS and self.trip[-1] == self.world.TERMINAL_NODE:
        self.direction = self.BACKWARDS
        # need to remove the last node here, which is the TERMINAL_NODE by
        # definition, since we're already there
        self.return_trip.pop()
        self.return_length = len(self.return_trip)

    # If we made it back home (NEST)
    if self.direction == self.BACKWARDS and self.trip[-1] == self.world.SOURCE_NODE:
        self.direction = self.FORWARDS
        self.history.append(self.trip)
        self.trip = [self.trip[-1]]
        self.return_trip = [self.trip[0]]
        self.return_length = None
  
  def choose(self):
    """Select the next node the ant travels to"""

    if self.direction == self.FORWARDS:
      # Get the pheremones on the arcs to each possible destination node
      pheromones = self.world.get_pheromones(self.trip[-1])

      # If there is more than one node available, don't go to the one you were
      # just at
      if len(self.trip) > 1 and self.trip[-2] in pheromones and len(pheromones) > 1:
        del pheromones[self.trip[-2]]

      nodes = pheromones.keys()
      levels = map(lambda i: i**alpha, pheromones.values())
      ranges = map(lambda i: float(sum(levels[:i+1])), range(len(levels)))

      # Get a random draw from a standard uniform distribution
      draw = uniform(0, sum(levels))

      # Get the number of the destination node
      index = [i for i in range(len(ranges)) if ranges[i] > draw][0]

      node = nodes[index]

      #if self.trip[-1] == NEST:
      #  print nodes, levels, ranges, draw, node

    else:
      node = self.return_trip.pop()

    return node

