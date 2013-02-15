from settings import *
from agent import Agent
from ant import Ant

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
    self.base         = { arc:0 for arc in self.arcs } # initial pheremone levels
    self.current      = self.base.copy() # pheromone changes for the period
    self.history      = [] # history of pheromone settings for each period
    self.memo         = { arc:1 for arc in self.arcs } # running tally of pheromones on nodes
    self.memo_history = [] # history of runny tally for each period

  def advance(self):
    for arc, level in self.current.iteritems():
      # add the new level
      self.memo[arc] += level
      # evaporate some pheremone
      self.memo[arc] = (1 - rho) * self.memo[arc]

    self.memo_history.append(self.memo.copy())
    self.history.append(self.current)
    self.current = self.base.copy()

  def get_ant(self, i):
    return self.ants[i]

  def get_pheromones(self, node):
    pheromones = {}
    for destination in self.graph[node]:
      pheromones[destination] = self.memo[node | destination]
    return pheromones

  def populate(self, ant):
    self.ants.append(ant)
    ant.attach(self)
    return len(self.ants)

  def update(self, ant):
    #print reverse_node(ant.trip[-1]), '|', reverse_node(ant.trip[-2])
    level = deposit / ant.return_length if autocatalysis else deposit
    self.current[ant.trip[-1] | ant.trip[-2]] += level
