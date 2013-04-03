# Default parameter values
graph = 'db' # the name of the graph to use
trials = 1              # number of trials
T = 1000                # number of steps
n = 2                   # number of ants
deposit = 1             # amount of pheromone to deposit
autocatalysis = False   # is deposit inversely related to found path length?
alpha = 1               # pheromone amplification
rho = 0.00              # evaporation rate

graphs = {
  # Double bridge
  'db': {
    'SOURCE_NODES':   ['NEST'],
    'TERMINAL_NODES': ['FOOD'],
    'GRAPH': {
      'NEST':        ['FOOD', 'LONG_BRANCH'],
      'LONG_BRANCH': ['NEST', 'FOOD'],
      'FOOD':        ['LONG_BRANCH', 'NEST']
    }
  },

  # Extended double bridge
  'edb': {
    'SOURCE_NODES':   ['NEST'],
    'TERMINAL_NODES': ['FOOD'],
    'GRAPH': {
      'NEST': ['A', 'H'],
      'A': ['NEST', 'B'],
      'B': ['A', 'C'],
      'C': ['B', 'D'],
      'D': ['C', 'E'],
      'E': ['D', 'F'],
      'F': ['E', 'G'],
      'G': ['F', 'FOOD'],
      'H': ['NEST', 'I'],
      'I': ['H', 'J', 'K', 'M'],
      'J': ['I', 'K',],
      'K': ['I', 'J', 'L', 'N'],
      'L': ['K', 'P', 'FOOD'],
      'M': ['I', 'N', 'O'],
      'N': ['K', 'M', 'P'],
      'O': ['H', 'M', 'P', 'Q'],
      'P': ['L', 'N', 'O', 'Q'],
      'Q': ['O', 'P']
    }
  },

  # Harder bridge
  'hard': {
    'SOURCE_NODES':   ['NEST'],
    'TERMINAL_NODES': ['FOOD'],
    'GRAPH': {
      'NEST': ['A', 'F', 'G'],
      'A': ['NEST', 'B'],
      'B': ['A', 'C'],
      'C': ['B', 'D'],
      'D': ['C', 'E'],
      'E': ['D', 'FOOD'],
      'F': ['NEST', 'G', 'K'],
      'G': ['NEST', 'F', 'H'],
      'H': ['F', 'G', 'I', 'J', 'K', 'L'],
      'I': ['H', 'J', 'FOOD'],
      'J': ['H', 'I', 'L', 'FOOD'],
      'K': ['F', 'H', 'L', 'M'],
      'L': ['H', 'J', 'K', 'M'],
      'M': ['K', 'L']
    }
  }
}