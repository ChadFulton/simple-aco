from world import World
from ant import Ant
import settings
import argparse, time

def simulate(n, T, graph, source_node, terminal_node):
  """Run an ant-colony optimization simulation"""

  # Instantiate the world
  world = World(graph, source_node = source_node, terminal_node = terminal_node)
  
  # Create the ants
  for i in range(n):
    world.populate(
      Ant(world, world.SOURCE_NODE)
    )

  # Make the ants move until convergence
  for t in range(T):
    for i in range(n):
      world.ants[i].move()
    world.advance()

  return world

def main():
  """Function called by running simulate.py on the command line"""
  t0 = time.time()

  path_lengths = {}
  p = []
  for i in range(settings.trials):
    world = simulate(settings.n, settings.T, graph=settings.double_bridge, source_node = settings.NEST, terminal_node = settings.FOOD);
    pheromones = world.memo_history[-1]
    p.append(float(pheromones[settings.NEST | settings.FOOD])**settings.alpha / (float(pheromones[settings.NEST | settings.FOOD])**settings.alpha + float(pheromones[settings.LONG_BRANCH | settings.NEST])**settings.alpha))
    for path_length, n in world.path_lengths.iteritems():
      if path_length not in path_lengths:
        path_lengths[path_length] = 0
      path_lengths[path_length] += n
  fail = [i for i in p if i <= 0.5]
  success = [i for i in p if i >= 0.5]

  t1 = time.time()

  print ''
  print 'Simple ACO - Simulation Results'
  print '==========================================='
  print '| trials = %d, T = %d, n = %d' % (settings.trials, settings.T, settings.n)
  print '| deposit = %.1f, alpha = %.1f, rho = %.1f' % (settings.deposit, settings.alpha, settings.rho)
  print '| Autocatalysis = %s' % str(settings.autocatalysis)
  print '|'
  print '| Convergence to long path: %d%%' % (float(len(fail)) / float(len(p))*100)
  print '| (in %.1f seconds)' % (t1-t0)
  print '| Number of paths found: ', path_lengths
  print '==========================================='
  print ''

if __name__ == "__main__":
  # Set up the command line arguments
  parser = argparse.ArgumentParser(description='Run Ant Colony Optimization simulation.')
  parser.add_argument('-i',
                      help='Number of trials (default=%d)' % settings.trials,
                      type=int, default = settings.trials
                     )
  parser.add_argument('-n',
                      help='Number of ants (default=%d)' % settings.n,
                      type=int, default = settings.n
                     )
  parser.add_argument('-T',
                      help='Number of steps each ant takes (default=%d)' % settings.T,
                      type=int, default = settings.T
                     )
  parser.add_argument('-d', '--deposit',
                      help='Amount of pheromone deposited at each step (default=%.1f)' % settings.deposit,
                      type=float, default = settings.deposit
                     )
  parser.add_argument('-a', '--alpha',
                      help='pheromone amplification parameter (default=%.1f)' % settings.alpha,
                      type=float, default = settings.alpha
                     )
  parser.add_argument('-r', '--rho',
                      help='Rate of pheromone evaporation (default=%.1f)' % settings.rho,
                      type=float, default = settings.rho
                     )
  parser.add_argument('-c', '--autocatalysis',
                      help='Is deposit inversely related to found path length? (default=%s)' % str(settings.autocatalysis),
                      action="store_true", default = settings.autocatalysis
                     )
  args = parser.parse_args()

  # Modify the global settings based on the given arguments
  for name in ['i', 'n', 'T', 'deposit', 'alpha', 'rho', 'autocatalysis']:
    setattr(settings, name, getattr(args, name))

  # Initialize the simulation
  main()
