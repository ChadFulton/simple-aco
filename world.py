from agent import Agent
from ant import Ant
import settings

from random import choice
from math import log

class World(Agent):

  def __init__(self, graph):
    super(World, self).__init__()

    # World population
    self.ants = []

    # World geography
    self.set_graph(graph)

    # World pheromone levels
    self.base         = { arc:0 for arc in self.arcs } # initial pheromone levels
    self.current      = self.base.copy() # pheromone changes for the period
    self.history      = [] # history of pheromone settings for each period
    self.memo         = { arc:1 for arc in self.arcs } # running tally of pheromones on nodes
    self.memo_history = [] # history of running tally for each period
    self.path_lengths = {} # running tally of path lengths found by the ants

  def advance(self):
    """Advance to the next time period"""
    for arc, level in self.current.iteritems():
      # add the new level
      self.memo[arc] += level
      # evaporate some pheromone
      if settings.rho:
        self.memo[arc] = (1 - settings.rho) * self.memo[arc]
    if sum(self.memo.values()) < 0.01:
      self.memo = { arc:1 for arc in self.arcs }

    #self.memo_history.append(self.memo.copy())
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

  def get_time(self):
    return len(self.history)-1

  def is_source(self, node):
    if not type(node) == int:
      node = self.map_node(node)
    return node in self.SOURCE_NODES

  def is_terminal(self, node):
    if not type(node) == int:
      node = self.map_node(node)
    return node in self.TERMINAL_NODES

  def map_node(self, id):
    """Maps a node name to a node integer or vice-versa"""

    # If we're given an integer, return a name
    if type(id) == int:
      return self.nodes[int(log(id) / log(2))];
    # Otherwise, return the integer corresponding to the node
    else:
      return 2**self.nodes.index(id)

  def populate(self, ant):
    """Add an ant to the world population"""
    ant.set_location(choice(self.SOURCE_NODES))
    self.ants.append(ant)
    ant.attach(self)
    return len(self.ants)

  def set_graph(self, graph):
    # Get the set of nodes
    self.nodes = []
    for start, ends in graph['GRAPH'].iteritems():
      if start not in self.nodes:
        self.nodes.append(start)
      for end in ends:
        if end not in self.nodes:
          self.nodes.append(end)

    # Create the usable graph, in terms of nodes as integers
    self.graph = {}
    for start, ends in graph['GRAPH'].iteritems():
      self.graph[self.map_node(start)] = map(self.map_node, ends)

    # Now we need to set the source and terminal nodes, in terms of integers
    self.SOURCE_NODES = map(self.map_node, graph['SOURCE_NODES'])
    self.TERMINAL_NODES = map(self.map_node, graph['TERMINAL_NODES'])

    # Get the set of arcs
    self.arcs = []
    for start, ends in graph['GRAPH'].iteritems():
      for end in ends:
          if self.map_node(start) | self.map_node(end) not in self.arcs:
            self.arcs.append(self.map_node(start) | self.map_node(end))

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
      if ant.trip[-2] in self.TERMINAL_NODES:
        if ant.return_length not in self.path_lengths:
          self.path_lengths[ant.return_length] = 0
        self.path_lengths[ant.return_length] += 1
