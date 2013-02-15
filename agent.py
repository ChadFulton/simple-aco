class Agent(object):
  """Generic agent class

  Implements the observer pattern.
  """

  def __init__(self):
    self._observers = []

  def attach(self, observer):
    if not observer in self._observers:
      self._observers.append(observer)

  def detach(self, observer):
    try:
      self._observers.remove(observer)
    except ValueError:
      pass

  def notify(self, modifier=None):
    for observer in self._observers:
      if modifier != observer:
        observer.update(self)

  def update():
    pass