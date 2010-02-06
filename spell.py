from focusable import Focusable

# This class makes sure pretty printing of spell-classes is done
class SpellMeta(type):
	def __str__(self):
		return '%s (%d)' % (self._name, self._cost)

class Spell(Focusable):
	__metaclass__ = SpellMeta
	def __init__(self, **kwargs):
		super(Spell, self).__init__(**kwargs)

	def cast(self, caster, targets):
		self.unfocus()
		self.func(caster, **targets)

	def cost(self, targets):
		if callable(self._cost):
			return self._cost(**targets)
		return self._cost

	def __str__(self):
		return '%s (%d)' % (self._name, self._cost)

def spell(desc=None, cost = 1, tags = ()):
	def spell_i(func):
		class _Spell(Spell):
			_desc = desc
			_cost = cost
			_name = func.func_name
			_htext = func.func_doc
			def __init__(self, **kwargs):
				super(_Spell, self).__init__(tags=tags, **kwargs)
				self.func = func
		return _Spell
		
	return spell_i
