from hook import Hookable
from owned import Owned
from error import IllegalMovement
from zone import zUnordered,zPublic
import operator

def friendly(a,b):
	return getattr(a, 'owner', None) == getattr(b, 'owner', None)

# TODO, come up with a real battle system
# * defence bonus from buildings
# * attack/defence bonus depending on enemies/allies
# * armour? damage soakers? user ctrl damage dealing?
# * also, hooks!

def deal_damage(units, amount):
	for x in units:
		target = min(x.hp - x.damage, amount)
		x.add_damage(target)
		amount -= target
		if amount == 0:
			break
	return amount

def battle(attackers, building):
	defenders = building.get_defenders()
	
	a = reduce(lambda s,d: s + d.get_attack(), attackers, 0)
	d = reduce(lambda s,d: s + d.get_defence(), defenders, 0)

	arest = deal_damage(defenders, a)
	drest = deal_damage(attackers, d)

	building.add_damage(arest)
	# do something with drest?

def move_creatures(creatures, building):
	""" Move all of @creatures to @building. it is required that all units share owner """

	is_attack = not friendly(building, creatures[0])

	# To move to a opposing building a free pad is required
	if is_attack and not len(building.free_pads()) > 0:
		raise IllegalMovement("No free pads")

	creatures = [x for x in creatures if x.run_hook('pre-move', building)[0]]
	creatures = filter(None, map(lambda x: x.position.remove_creature(x), creatures))
	creatures = filter(None, map(lambda x: building.add_creature(x), creatures))

	for x in creatures:
		x.position = building

	if is_attack:
		battle(creatures, building)

class CreatureStack(zUnordered, zPublic): pass

# This class makes sure pretty printing of creature-classes is done
class CreatureMeta(type):
	def __str__(self):
		return '%s (%d/%d/%d) %d' % (self.__name__, self.base_atk, self.base_def, self.hp, self.cost)

class Creature(Hookable):
	__metaclass__ = CreatureMeta
	base_atk = 0
	base_def = 0
	hp = 1
	levels = ()
	cost = 1
	def __init__(self, damage = 0, xp = 0, position = None, **kwargs):
		self.damage = damage
		self.position = position
		self.xp = xp
		super(Creature, self).__init__(**kwargs)

	def get_level_bonus(self):
		for xp,a,d in self.levels[::-1]:
			if xp <= self.xp:
				return a,d
		return 0,0

	def get_attack(self):
		a,d = self.get_level_bonus()
		return self.base_atk + a

	def get_defence(self):
		a,d = self.get_level_bonus()
		return self.base_def + d

	def add_damage(self, amount):
		self.damage += amount

	def heal(self, source, amount):
		source, amount = self.run_hook('pre-heal', source, amount)
		if source and amount:
			self.damage = max(self.damage - amount, 0)
			print "%s was healed for %s by %s" % (self, amount, source)
			self.run_hook('post-heal', source, amount)
		return source, amount

	def gain_xp(self, amount):
		amount = self.run_hook('pre-gain-xp', amount)
		if amount:
			self.xp += amount
			self.run_hook('post-gain-xp', amount)

	def give_xp(self):
		return max(self.xp * 0.1, 10)

	def move(self, building):
		building = self.run_hook('pre-move', building)
		building.add_creature(self)
		self.run_hook('post-move', building)

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
