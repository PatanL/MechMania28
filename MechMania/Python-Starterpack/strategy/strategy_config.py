from strategy.archer_strategy_3 import ArcherStrategy
from strategy.knight_scope import KnightScope
from strategy.starter_strategy import StarterStrategy
from strategy.wizard_rush import WizardRush
from strategy.strategy import Strategy
from strategy.archer_strategy_3 import ArcherStrategy
from strategy.archer_shield import ArcherShieldStrategy

"""Return the strategy that your bot should use.

:param playerIndex: A player index that can be used if necessary.

:returns: A Strategy object.
"""
def get_strategy(player_index: int) -> Strategy:
  if(player_index % 2 == 0):
    return ArcherStrategy()
  else:
    return ArcherShieldStrategy()
  #return ArcherStrategy()
  #return KnightScope()
  #return WizardRush();
  #return StarterStrategy()