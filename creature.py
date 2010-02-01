from hook import Hookable
from zone import zUnordered,zPublic

class CreatureStack(zUnordered, zPublic): pass

# This class makes sure pretty printing of creature-classes is done
class CreatureMeta(type):
	def __str__(self):
		return '%s (%d/%d/%d) %d' % (self.__name__, self.attack, self.defence, self.hp, self.cost)

class Creature(Hookable):
	__metaclass__ = CreatureMeta
	attack = 0
	defence = 0
	hp = 1
	cost = 1
	def __init__(self, damage = 0, position = None, **kwargs):
		self.damage = damage
		self.position = position
		super(Creature, self).__init__(**kwargs)

	def get_attack(self):
		(attack,) = self.run_hook('pre-get-attack', self.attack)
		self.run_hook('post-get-attack', attack)
		return attack

	def get_defence(self):
		(defence,) = self.run_hook('pre-get-defence', self.defence)
		self.run_hook('post-get-defence', defence)
		return defence

	def add_damage(self, amount):
		self.damage += amount

	def heal(self, source, amount):
		source, amount = self.run_hook('pre-heal', source, amount)
		if source and amount:
			self.damage = max(self.damage - amount, 0)
			print "%s was healed for %s by %s" % (self, amount, source)
			self.run_hook('post-heal', source, amount)
		return source, amount

	def move(self, building):
		building = self.run_hook('pre-move', building)
		building.add_creature(self)
		self.run_hook('post-move', building)
