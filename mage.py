from zone import zRandom,zUnordered,zPrivate,zPublic
from building import ManaRuby
from spell import Spell
from hook import Hookable
from creature import move_creatures

FOCUS_SIZE = 5

class Mage(Hookable):
	class Library(zUnordered, zPublic): pass
	class Focused(zUnordered, zPrivate): pass
	class Pool(zRandom, zPrivate): pass

	def __init__(self, **kwargs):
		super(Mage, self).__init__(**kwargs)
		self.library = Mage.Library(owner=self)
		self.focused = Mage.Focused(owner=self)

		self.creatures = []

	def build_pool(self):
		pool = Mage.Pool(owner=self)
		pool.extend(self.library)
		(pool, ) = self.run_hook('pre-build-pool', pool)
		assert isinstance(pool, Mage.Pool)
		self.run_hook('post-build-pool', pool)

		return pool

	def focus(self):
		pool = self.build_pool()
		self.focused[:] = pool.get(FOCUS_SIZE)

	def focused_spells(self):
		return [x for x in self.focused if isinstance(x,Spell)]
	
	def focused_mana(self):
		return [x for x in self.focused if isinstance(x,ManaRuby.ManaShard)]

	def cast_spell(self, spell, targets):
		cost = spell.cost(targets)
		spell.cast(self, targets)

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
