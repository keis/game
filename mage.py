from zone import zRandom,zUnordered,zPrivate,zPublic
from buildings import ManaRuby
from spell import Spell
from hook import Hookable
from act import move_creatures
from error import NotEnoughMana
from xselect import select

FOCUS_SIZE = 5

class Mage(Hookable):
	class Library(zUnordered, zPublic): pass
	class Focused(zUnordered, zPrivate): pass
	class Pool(zRandom, zPrivate): pass
	class Summary(list): pass

	def __init__(self, name='Rincewind', **kwargs):
		super(Mage, self).__init__(**kwargs)
		self.name = name
		self.library = Mage.Library(owner=self)
		self.focused = Mage.Focused(owner=self)
		self.pool = Mage.Pool(owner=self)

		# replace with set of all owned stuff?
		self.creatures = Mage.Summary()
		self.buildings = Mage.Summary()

		self.mana = 0

	def __children(self):
		return [self.library, self.focused, self.core, self.buildings, self.creatures]

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

		self.pool = pool

	def focus(self):
		pool = self.pool
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

	def discard(self, count, desc=None):
		# TODO: Make it possible to choose which focusables to discard
		focused = self.focused
		if desc:
			focused = select(desc, focused)

		if len(focused) < count:
			return False

		for x in focused[:count]:
			x.discard()

		return True

	def sacrifice(self, count, desc=None):
		pool = self.build_pool()
		if desc is not None:
			pool = select(desc, pool)

		if len(pool) < count:
			return False

		for x in pool[:count]:
			x.sacrifice()

		return True

	def __getitem__(self, index):
		return self.__children()[index]

	def __len__(self):
		return len(self.__children())
