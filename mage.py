from zone import zRandom,zUnordered,zPrivate,zPublic
from buildings import ManaRuby
from spell import Spell
from hook import Hookable
from act import move_creatures
from error import NotEnoughMana

FOCUS_SIZE = 5

class Mage(Hookable):
	class Library(zUnordered, zPublic): pass
	class Focused(zUnordered, zPrivate): pass
	class Pool(zRandom, zPrivate): pass

	def __init__(self, **kwargs):
		super(Mage, self).__init__(**kwargs)
		self.library = Mage.Library(owner=self)
		self.focused = Mage.Focused(owner=self)

		# replace with set of all owned stuff?
		self.creatures = []
		self.buildings = []

		self.mana = 0

	def add_creature(self, creature):
		self.creatures.append(creature)

	def remove_creature(self, creature):
		self.creatures.remove(creature)

	def add_building(self, building):
		self.buildings.append(building)

	def remove_building(self, building):
		self.buildings.remove(building)

	def build_pool(self):
		pool = Mage.Pool(owner=self)
		pool.extend(self.library)
		(pool, ) = self.run_hook('pre-build-pool', pool)
		assert isinstance(pool, Mage.Pool)
		self.run_hook('post-build-pool', pool)

		return pool

	def focus(self):
		pool = self.build_pool()
		focused = pool.get(FOCUS_SIZE)
		(pool, focused) = self.run_hook('pre-focus', pool, focused)
		self.focused[:] = focused
		self.run_hook('post-focus', pool, focused)

		self.convert_mana()

	def convert_mana(self):
		mana = self.focused_mana()
		self.mana = reduce(lambda a,b: a + b.capacity, mana, 0)

	def focused_spells(self):
		return [x for x in self.focused if isinstance(x,Spell)]
	
	def focused_mana(self):
		return [x for x in self.focused if isinstance(x,ManaRuby.ManaShard)]

	def cast_spell(self, spell, targets):
		cost = spell.cost(targets)
		if cost <= self.mana:
			self.mana -= cost
			spell.cast(self, targets)
		else:
			raise NotEnoughMana("%s < %s" % (self.mana, cost))

	def order_movement(self, units, target):
		move_creatures(units, target)

	def discard(self, count, tag=None):
		# TODO: Make it possible to choose which focusables to discard
		focused = self.focused
		if tag:
			focused = [x for x in focused if tag in x.tags]

		if len(focused) < count:
			return False

		for x in focused[:count]:
			x.discard()

		return True
