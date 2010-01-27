from creature import Creature
from owned import Owned
from channeler import Channeler

class LizardDemon(Creature, Owned):
	base_atk = 20
	base_def = 25
	hp = 100
	levels = ((50, 5, 5), (100, 10, 8), (170, 14, 10))
	cost = 1

	def __init__(self, **kwargs):
		super(LizardDemon, self).__init__(**kwargs)

class Skeleton(Creature, Owned):
	base_atk = 20
	base_def = 20
	hp = 80
	levels = ()
	cost = 1

	def __init__(self, **kwargs):
		super(Skeleton, self).__init__(**kwargs)
		self.add_hook('pre-gain-xp', lambda t,a: 0)

class Adventurer(Creature, Owned):
	base_atk = 15
	base_def = 15
	hp = 90
	levels = ((10, 5, 5), (20, 6, 9), (50, 10, 15), (100, 15, 25), (200, 30, 40), (300, 50, 40), (400, 100, 100))
	cost = 2

	def __init__(self, **kwargs):
		super(Adventurer, self).__init__(**kwargs)
		self.add_hook('pre-gain-xp', lambda a: a * 1.5)

class Summoner(Creature, Channeler):
	base_atk = 10
	base_def = 10
	hp = 40
	levels = ((10, 5, 5),)

	def __init__(self, **kwargs):
		from spell import summon
		super(Summoner, self).__init__(**kwargs)
		self.add(summon(owner=self.owner))
