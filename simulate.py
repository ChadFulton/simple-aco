from world import World
from ant import Ant
import settings
import argparse, time

def simulate(trials, n, T, graph):
  """Run i trials of an ant-colony optimization simulation"""

  worlds = []
  for j in range(trials):
    # Instantiate the world
    world = World(graph)
    
    # Create the ants
    for i in range(n):
      world.populate(
        Ant(world)
      )

    # Make the ants move until convergence
    for t in range(T):
      for i in range(n):
        world.ants[i].move()
      world.advance()

    worlds.append(world)

  return worlds

def main(profile=False):
  """Function called by running simulate.py on the command line"""
  t0 = time.time()

  # Results from the simulations
  history = []
  worlds = simulate(settings.trials, settings.n, settings.T, graph=settings.graphs[settings.graph]);
  history.append({k:round(float(v)/float(sum(worlds[-1].path_lengths.values())), 2)*100 for k,v in worlds[-1].path_lengths.iteritems()})

  t1 = time.time()

  if not profile:
    print ''
    print 'Simple ACO - Simulation Results (in %.1f seconds)' % (t1-t0)
    print '==========================================='
    print '| trials = %d, T = %d, n = %d' % (settings.trials, settings.T, settings.n)
    print '| deposit = %.1f, alpha = %.2f, rho = %.2f' % (settings.deposit, settings.alpha, settings.rho)
    print '| Autocatalysis = %s' % str(settings.autocatalysis)
    print '|'
    print '| Convergence to the shortest path %0.f%% ' % (history[-1][min(history[-1].keys())] / sum(history[-1].values())*100.0)
    print '| Pct of traversals by path length: ', history[-1]
    print '==========================================='
    print ''

if __name__ == "__main__":
  # Set up the command line arguments
  parser = argparse.ArgumentParser(description='Run Ant Colony Optimization simulation.')
  parser.add_argument('-g', '--graph',
                      help='Graph to use (default=%s)' % settings.graph,
                      default = settings.graph, choices=settings.graphs.keys()
                     )
  parser.add_argument('-i', '--trials',
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
  parser.add_argument('-p', '--profile',
                      help='Profile the ACO simulation? (default=%s)' % str(False),
                      action="store_true", default = False
                     )
  args = parser.parse_args()

  # Modify the global settings based on the given arguments
  for name in ['graph', 'trials', 'n', 'T', 'deposit', 'alpha', 'rho', 'autocatalysis']:
    setattr(settings, name, getattr(args, name))

  # Initialize the simulation
  if args.profile:
    import cProfile
    cProfile.run('main(True)')
  else:
    main();
