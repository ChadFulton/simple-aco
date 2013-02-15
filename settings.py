# Define some constants
NEST = 1
FOOD = 2
LONG_BRANCH = 4

def reverse_node(node):
  if node == NEST:
    return 'NEST'
  if node == FOOD:
    return 'FOOD'
  if node == LONG_BRANCH:
    return 'LONG_BRANCH'

# Default parameter values
trials = 100          # number of trials
T = 1000              # number of steps
n = 2                 # number of ants
deposit = 1           # amount of pheremone to deposit
autocatalysis = False # is deposit inversely related to found path length?
alpha = 1             # pheromone amplification
rho = 0.00            # evaporation

# Graphs
double_bridge = {
  NEST:        [FOOD, LONG_BRANCH],
  LONG_BRANCH: [NEST, FOOD],
  FOOD:        [LONG_BRANCH, NEST]
}