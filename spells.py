from spell import spell,Timer
import effects

@spell(desc={'spell': ("the spell to prepare", "spells")}, cost = 1)
def prepare_spell(caster, spell=None):
	"""Makes a new spell ready to be used"""
	caster.library.add(spell(owner=caster))

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
		building = building_type(owner=caster)
		parent,pos = pad
		parent.connect(building, pos)
		caster.add_building(building)

@spell(desc={
		'creature_type': ("the kind of creature to summon", "creature_types"),
		'building': ("the building to summon the creature at", "buildings")
	}, cost = 5, tags=('create',))
def summon(caster, creature_type=None, building=None):
	cost = creature_type.cost - 1
	if caster.discard(cost, tag='create'):
		creature = creature_type(owner=caster, position=building)
		building.add_creature(creature)
		caster.add_creature(creature)

@spell(desc={
		'building': ("The building to initiate the fire storm at", "op_buildings")
	}, cost=10)
def fire_storm(caster, building=None):
	t = Timer(owner=caster, target=3)

	def _fire_storm(b, power):
		b.add_damage(power)
		b.add_hook('pre-repair', lambda s,a: (s, a * 0.5), owner=t)
		for u in b.units:
			u.add_damage(power * 0.2)
			u.add_hook('pre-heal', lambda s,a: (s, a * 0.5), owner=t)
		
	building.apply_aoe(_fire_storm, lambda c, x: x * 0.8, 100)
