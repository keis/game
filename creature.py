from hook import Hookable
from zone import zUnordered,zPublic
from owned import friendly

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
	stealthed = False
	can_stealth = False

	def __init__(self, damage = 0, position = None, **kwargs):
		self.damage = damage
		self.position = position
		super(Creature, self).__init__(**kwargs)

		if self.can_stealth:
			self.add_global_hook('start-of-turn', self._go_stealthed)

	def _go_stealthed(self, t, player):
		if not self.stealthed:
			self.run_hook('pre-stealth')
			self.stealthed = True
			self.run_hook('post-stealth')

	def get_attack(self):
		(attack,) = self.run_hook('pre-get-attack', self.attack)
		self.run_hook('post-get-attack', attack)
		return attack

	def get_defence(self):
		(defence,) = self.run_hook('pre-get-defence', self.defence)
		self.run_hook('post-get-defence', defence)
		return defence

	def add_damage(self, amount):
		(amount,) = self.run_hook('pre-add-damage', amount)
		self.damage += amount
		self.run_hook('post-add-damage', amount)
		if self.damage >= self.hp:
			self.destroy()

	def destroy(self):
		self.run_hook('pre-destroy')
		self.position.remove_creature(self)
		if hasattr(self, 'owner'):
			self.owner.remove_creature(self)
		self.run_hook('post-destroy')
		self._cleanup()

	def heal(self, source, amount):
		source, amount = self.run_hook('pre-heal', source, amount)
		if source and amount:
			self.damage = max(self.damage - amount, 0)
			self.run_hook('post-heal', source, amount)
		return source, amount

	def move(self, building):
		building = self.run_hook('pre-move', building)
		building.add_creature(self)
		self.run_hook('post-move', building)

	def _cleanup(self):
		try: cleanup = super(Creature, self)._cleanup
		except AttributeError: pass
		else: cleanup()
