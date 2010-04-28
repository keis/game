from zone import zRandom,zUnordered,zPrivate,zPublic
from buildings import ManaRuby
from spell import Spell
from hook import Hookable
from error import NotEnoughMana
from xselect import select

FOCUS_SIZE = 5

class Mage(Hookable):
	class Library(zUnordered, zPublic): pass
	class Focused(zUnordered, zPrivate): pass
	class Pool(zRandom, zPrivate): pass
	class Summary(list): pass

	def __init__(self, name='Rincewind', context=None, IDs=None, **kwargs):
		super(Mage, self).__init__(**kwargs)
		self.name = name
		self.context = context
		self.IDs = IDs
		self.library = Mage.Library(owner=self)
		self.focused = Mage.Focused(owner=self)
		self.pool = Mage.Pool(owner=self)

		# replace with set of all owned stuff?
		self.creatures = Mage.Summary()
		self.buildings = Mage.Summary()

		self.mana = 0

	def build_IDs(self):
		tmp = {
			'self' : self,
			'opponent' : [x for x in select('> Mage', self.context) if not x is self][0]
		}
		tmp.update(self.IDs)
		return tmp

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
		print 'HOE', self.pool

	def focus(self):
		def have_mana():
			return any(isinstance(x, ManaRuby.ManaShard) for x in focused)

		def have_spell():
			return any(isinstance(x, Spell) for x in focused)

		pool = self.pool

		# TODO, make sure there is atleast one spell and manashard in the pool
		# or limit the number of attempts
		while True:
			if pool == []:
				break
			focused = pool.get(FOCUS_SIZE)
			(pool, focused) = self.run_hook('pre-focus', pool, focused)

			if not (have_mana() and have_spell()):
				print 'mulligan', focused
				continue

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
