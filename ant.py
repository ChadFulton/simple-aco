from agent import Agent
from random import uniform
import settings

class Ant(Agent):
  FORWARDS  = 0
  BACKWARDS = 1

  def __init__(self, world, location, direction = None):
    super(Ant, self).__init__()

    self.world = world;

    self.direction      = direction or self.FORWARDS
    self.history        = []          # a list of trips
    self.trip           = [location]  # a list of nodes forming a complete cycle
    self.return_trip    = [location]  # the complete trip cycle, without loops
    self.return_length  = None        # the final return trip length

  def move(self):
    """Move the ant"""

    # 1. Move the ant
    next = self.choose()
    self.trip.append(next)

    # 2. Let the observers know there the ant moved
    self.notify()

    # 3. Update the ant's memory (add return trip information)
    if self.direction == self.FORWARDS:
      self.return_trip.append(self.trip[-1])
      # Check for and remove cycles in the return trip
      index = self.return_trip.index(self.trip[-1])
      if index != len(self.return_trip)-1:
        self.return_trip = self.return_trip[:index+1]


    # 4. Check if we reached a destination and need to turn the ant around
    # If we made it to the destination (FOOD)
    if self.direction == self.FORWARDS and self.trip[-1] == self.world.TERMINAL_NODE:
        self.direction = self.BACKWARDS
        # We need to remove the last node on the return trip, which is the
        # TERMINAL_NODE by definition, since we're already there
        self.return_trip.pop()
        # We have to save the return length here because when we traverse the
        # path back to the nest, we'll lose the total length of the trip when
        # we pop() the list.
        self.return_length = len(self.return_trip)

    # If we made it back home (NEST)
    if self.direction == self.BACKWARDS and self.trip[-1] == self.world.SOURCE_NODE:
        self.direction = self.FORWARDS
        # Save the trip just made, and reset the current trip to an empty one
        self.history.append(self.trip)
        self.trip = [self.trip[-1]]
        self.return_trip = [self.trip[0]]
        self.return_length = None
  
  def choose(self):
    """Select the next node the ant travels to"""

    # If we're going towards the destination, make a probabilistic choice
    if self.direction == self.FORWARDS:

      # Get the pheromones on the arcs to each possible destination node
      pheromones = self.world.get_pheromones(self.trip[-1])

      # If there is more than one node available, don't go to the one you were
      # just at
      if len(self.trip) > 1 and self.trip[-2] in pheromones and len(pheromones) > 1:
        del pheromones[self.trip[-2]]

      # Modify the pheromone levels to reflect pheromone amplification
      levels = map(lambda i: i**settings.alpha, pheromones.values())

      # Map the pheromone levels of each node to cut points relative to the
      # total pheromone placed on all nodes together.
      cuts = map(lambda i: float(sum(levels[:i+1])), range(len(levels)))

      # Get a random draw from a standard uniform distribution
      draw = uniform(0, sum(levels))

      # Get the index of the cut point that corresponds to the random draw
      index = [i for i in range(len(cuts)) if cuts[i] > draw][0]

      # Get a mapping from the index of the cut points to the node ids
      nodes = pheromones.keys()

      # Map the index of the cut point to the node it represents
      node = nodes[index]

    # If we're going back home, just go back the way we came
    else:
      node = self.return_trip.pop()

    return node

