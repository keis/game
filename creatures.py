from creature import Creature
from owned import Owned
from channeler import Channeler
from random import random

class LizardDemon(Creature, Owned):
	attack = 20
	defence = 25
	hp = 100
	cost = 1

	def __init__(self, **kwargs):
		super(LizardDemon, self).__init__(**kwargs)

class Skeleton(Creature, Owned):
	attack = 20
	defence = 20
	hp = 80
	cost = 1

	def __init__(self, **kwargs):
		super(Skeleton, self).__init__(**kwargs)

class Summoner(Creature, Channeler):
	attack = 10
	defence = 10
	hp = 40

	def __init__(self, **kwargs):
		from spells import summon
		super(Summoner, self).__init__(**kwargs)
		self.add(summon(owner=self.owner))

class ManaEater(Creature, Owned):
	attack = 10
	defence = 10
	hp = 80
	cost = 2

	def __init__(self, **kwargs):
		super(ManaEater, self).__init__(**kwargs)
		self.power = 0

		self.owner.add_hook('post-focus', self.__post_focus_cb)
		self.add_hook('pre-get-attack', lambda a: a + self.power / 2)
		self.add_hook('pre-get-defence', lambda d: d + self.power / 3)

	def __post_focus_cb(self, pool, focused):
		from buildings import ManaRuby
		for x in focused:
			if isinstance(x, ManaRuby.ManaShard) and random() > 0.75:
				x.discard()
				self.power += x.capacity
