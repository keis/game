from mage import Mage
from spells import prepare_spell, focus_spell, fire_storm, repair, summon, construct, fire_storm
from buildings import SmallManaRuby,MediumManaRuby,LargeManaRuby,Core,Boulder
from creatures import LizardDemon, Skeleton, Ghost, Summoner, ManaEater
from hook import HookDB

import random
random.seed()

spells = (prepare_spell, focus_spell, repair, summon, construct, fire_storm)
creatures = (LizardDemon, Skeleton, Ghost, Summoner, ManaEater)
buildings = (SmallManaRuby, MediumManaRuby, LargeManaRuby, Boulder)
enabled = (spells, creatures, buildings)

test_spell = summon
test_creature = Ghost
test_building = Boulder

starting_spells = (prepare_spell, prepare_spell, prepare_spell,
	focus_spell, focus_spell,
	test_spell, test_spell, test_spell,
)

hook_db = HookDB()

next_player_id = 0
def create_player():
	global next_player_id
	m = Mage(name='player%s' % next_player_id, hook_db = hook_db, context = context, IDs = ids)
	rubies = [MediumManaRuby(owner=m, hook_db=hook_db) for x in range(3)]
	m.core = Core(owner=m)
	spells = [x(owner=m) for x in starting_spells]
	m.library.add(spells)

	map(m.core.connect, rubies)
	context.append(m)
	players.append(m)

	test = test_building(owner=m)
	rubies[0].connect(test)
	m.add_building(test)

	l = test_creature(owner=m, position=m.core)
	m.add_creature(l)
	m.core.add_creature(l)
	map(m.add_building, [m.core] + rubies)

	m.build_pool()
	m.focus()

	next_player_id += 1
	return m

context = [enabled]
ids = {'enabled': enabled}
players = []
