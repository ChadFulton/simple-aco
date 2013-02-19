from agent import Agent
from ant import Ant
import settings

class World(Agent):

  def __init__(self, graph, source_node, terminal_node):
    super(World, self).__init__()

    # World population
    self.ants = []

    # World geography
    self.graph          = graph
    self.SOURCE_NODE    = source_node
    self.TERMINAL_NODE  = terminal_node
    self.arcs = []
    for start, ends in self.graph.iteritems():
      for end in ends:
          if start | end not in self.arcs:
            self.arcs.append(start | end)

    # World pheromone levels
    self.base         = { arc:0 for arc in self.arcs } # initial pheromone levels
    self.current      = self.base.copy() # pheromone changes for the period
    self.history      = [] # history of pheromone settings for each period
    self.memo         = { arc:1 for arc in self.arcs } # running tally of pheromones on nodes
    self.memo_history = [] # history of running tally for each period
    self.path_lengths = {} # history of path lengths found by the ants

  def advance(self):
    """Advance to the next time period"""
    for arc, level in self.current.iteritems():
      # add the new level
      self.memo[arc] += level
      # evaporate some pheromone
      self.memo[arc] = (1 - settings.rho) * self.memo[arc]

    self.memo_history.append(self.memo.copy())
    self.history.append(self.current)
    self.current = self.base.copy()

  def get_ant(self, i):
    """Get the ith ant"""
    return self.ants[i]

  def get_pheromones(self, node):
    """Get the pheromones on all arcs proceeding from a given node"""
    pheromones = {}
    for destination in self.graph[node]:
      pheromones[destination] = self.memo[node | destination]
    return pheromones

  def populate(self, ant):
    """Add an ant to the world population"""
    self.ants.append(ant)
    ant.attach(self)
    return len(self.ants)

  def update(self, ant):
    """Observer pattern update method

    Update pheromone levels when an ant moves across an arc, and, after the ant
    completes the journey to the destination (FOOD), store the length of the
    path they found.
    """

    # Only want to update pheromone on the return journey
    if ant.direction == ant.BACKWARDS:
      # Check if we want the amount of pheromone to inversely correspond to path length
      level = settings.deposit / ant.return_length if settings.autocatalysis else settings.deposit
      self.current[ant.trip[-1] | ant.trip[-2]] += level

      # Save the path length if the ant just left the TERMINAL_NODE
      # (i.e. trip[-1] is the first node the ant went to after leaving the
      # TERMINAL_NODE, so trip[-2] would be the TERMINAL_NODE)
      if ant.trip[-2] == self.TERMINAL_NODE:
        if ant.return_length not in self.path_lengths:
          self.path_lengths[ant.return_length] = 0
        self.path_lengths[ant.return_length] += 1
