from hook import Hookable
from zone import zUnordered,zPublic

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
