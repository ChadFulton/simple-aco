from settings import *
from world import World
from ant import Ant

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

def main(n):
  p = []
  for i in range(100):
    world = simulate(n)
    pheromones = world.memo_history[-1]
    p.append(float(pheromones[NEST | FOOD])**alpha / (float(pheromones[NEST | FOOD])**alpha + float(pheromones[LONG_BRANCH | NEST])**alpha))
  fail = [i for i in p if i <= 0.5]
  success = [i for i in p if i >= 0.5]

  print 'Convergence to long path: ', (float(len(fail)) / float(len(p)))

if __name__ == "__main__":
    import sys
    args = {
      'n': int(sys.argv[1]) if len(sys.argv) > 1 else n,
    }
    main(**args)