from focusable import Focusable
import effects

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

@spell(desc={'spell': ("the spell to prepare", "spells")}, cost = 1)
def prepare_spell(caster, spell=None):
	"""Makes a new spell ready to be used"""
	caster.library.add(spell(owner=caster, hook_db = caster._hook_db))

@spell(desc={'spell': ("the spell to focus", "library")}, cost = 2)
def focus_spell(caster, spell=None):
	""" Brings a spell into focus"""
	spell.focus()

@spell(desc={'building': ("the building to initiate the repair at", "buildings")}, cost=10)
def repair(caster, building=None):
	effects.repair(caster, building)

@spell(desc={
		'building_type': ("the kind of building to construct", "building_types"),
		'pad': ("the pad to place the building on", "free_pads")
	}, cost = 5, tags=('create',))
def construct(caster, building_type=None, pad=None):
	cost = building_type.cost - 1
	if caster.discard(cost, tag='create'):
		building = building_type(owner=caster, hook_db = caster._hook_db)
		parent,pos = pad
		parent.connect(building, pos)

@spell(desc={
		'creature_type': ("the kind of creature to summon", "creature_types"),
		'building': ("the building to summon the creature at", "buildings")
	}, cost = 5, tags=('create',))
def summon(caster, creature_type=None, building=None):
	cost = creature_type.cost - 1
	if caster.discard(cost, tag='create'):
		creature = creature_type(owner=caster, position=building, hook_db = caster._hook_db)
		building.add_creature(creature)
		caster.creatures.append(creature)



@spell(desc={'target1': ("he who shall be nuked", "players")}, cost = 2)
def magic_arrow(caster, target1=None):
	"""Blasts a target with a mighty missile of magic energy"""
	print "WOOO, magic arrow"
