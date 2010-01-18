from zone import zRandom,zUnordered,zPrivate
from building import ManaRuby
from spell import Spell
from hook import Hookable
from creature import move_creatures

class Mage(Hookable):
	class Library(zRandom, zPrivate): pass
	class Focused(zUnordered, zPrivate): pass
	def __init__(self, **kwargs):
		super(Mage, self).__init__(**kwargs)
		self.library = Mage.Library(owner=self)
		self.focused = Mage.Focused(owner=self)

		self.creatures = []

	def focus(self):
		self.library.add(self.focused)
		self.focused.clear()
		self.focused.add(self.library.get(5))

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
