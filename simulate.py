from settings import *
from world import World
from ant import Ant
import argparse, time

def simulate(n):
  """Run an ant-colony optimization simulation"""

  # Instantiate the world
  world = World(double_bridge, source_node = NEST, terminal_node = FOOD)
  
  # Create the ants
  for i in range(n):
    world.populate(Ant(world, world.SOURCE_NODE))

  # Make the ants move until convergence
  for t in range(T):
    for i in range(n):
      world.ants[i].move()
    world.advance()

  return world

def main():
  t0 = time.time()

  p = []
  for i in range(trials):
    world = simulate(n)
    pheromones = world.memo_history[-1]
    p.append(float(pheromones[NEST | FOOD])**alpha / (float(pheromones[NEST | FOOD])**alpha + float(pheromones[LONG_BRANCH | NEST])**alpha))
  fail = [i for i in p if i <= 0.5]
  success = [i for i in p if i >= 0.5]

  t1 = time.time()

  print ''
  print 'Simple ACO - Simulation Results'
  print '==========================================='
  print '| trials = %d, T = %d, n = %d' % (trials, T, n)
  print '| deposit = %.1f, alpha = %.1f, rho = %.1f' % (deposit, alpha, rho)
  print '| Autocatalysis = %s' % str(autocatalysis)
  print '|'
  print '| Convergence to long path: %d%%' % (float(len(fail)) / float(len(p))*100)
  print '| (in %.1f seconds)' % (t1-t0)
  print '==========================================='
  print ''

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Run Ant Colony Optimization simulation.')
  parser.add_argument('-i', help='Number of trials (default=%d)' % trials, type=int, default = trials)
  parser.add_argument('-n', help='Number of ants (default=%d)' % n, type=int, default = n)
  parser.add_argument('-T', help='Number of steps each ant takes (default=%d)' % T, type=int, default = T)
  parser.add_argument('-d', '--deposit', help='Amount of pheremone deposited at each step (default=%.1f)' % deposit, type=float, default = deposit)
  parser.add_argument('-a', '--alpha', help='Pheremone amplification parameter (default=%.1f)' % alpha, type=float, default = alpha)
  parser.add_argument('-r', '--rho', help='Rate of pheromone evaporation (default=%.1f)' % rho, type=float, default = rho)
  parser.add_argument('-c', '--autocatalysis', help='Is deposit inversely related to found path length? (default=%s)' % str(autocatalysis), action="store_true", default = autocatalysis)
  args = parser.parse_args()

  trials = args.i
  n = args.n
  T = args.T
  deposit = args.deposit
  alpha = args.alpha
  rho = args.rho
  autocatalysis = args.autocatalysis

  main()
