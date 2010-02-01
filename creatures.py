from creature import Creature
from owned import Owned
from channeler import Channeler

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
		from spell import summon
		super(Summoner, self).__init__(**kwargs)
		self.add(summon(owner=self.owner))
