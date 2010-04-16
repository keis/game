from focusable import Focusable
from owned import Owned

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

class SpellToken(Owned):
	def __init__(self, **kwargs):
		super(SpellToken, self).__init__(**kwargs)

	def destroy(self):
		self._cleanup()

class Timer(SpellToken):
	def __init__(self, target=0, hook='start-of-turn', **kwargs):
		super(Timer, self).__init__(**kwargs)
		self.counter = 0
		self.target = target
		self.add_global_hook(hook, self.__cb)

	def __cb(self, *any):
		self.counter += 1
		if self.counter == self.target:
			self.destroy()

def spell(desc=None, cost = 1, sacrifice = None, tags = ()):
	def spell_i(func):
		class _Spell(Spell):
			_desc = desc			# dictionary containing description of needed parameters
			_cost = cost			# cost to cast the spell
			_sacrifice = sacrifice	# needed sacrifice when prepering spell
			_name = func.func_name	# name of spell (function name)
			_htext = func.func_doc	# short text describing the spell (function help)

			def __init__(self, **kwargs):
				super(_Spell, self).__init__(tags=tags, **kwargs)
				self.func = func
		return _Spell
		
	return spell_i
