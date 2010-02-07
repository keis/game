from mage import Mage
from spells import prepare_spell, focus_spell, fire_storm, repair, summon, construct, fire_storm
from buildings import SmallManaRuby,MediumManaRuby,LargeManaRuby,Core,Boulder
from creatures import LizardDemon, Skeleton, Summoner, ManaEater
from hook import HookDB

import random
random.seed()

spells = (prepare_spell, focus_spell, repair, summon, construct, fire_storm)
creatures = (LizardDemon, Skeleton, Summoner, ManaEater)
buildings = (SmallManaRuby, MediumManaRuby, LargeManaRuby, Boulder)

starting_spells = (prepare_spell, prepare_spell, prepare_spell,
	summon, summon, summon,
	construct, construct,
	focus_spell, focus_spell)

hook_db = HookDB()

def create_player():
	m = Mage(hook_db = hook_db)
	rubies = [MediumManaRuby(owner=m, hook_db=hook_db) for x in range(4)]
	m.core = Core(owner=m, hook_db=hook_db)
	spells = [x(owner=m, hook_db=hook_db) for x in starting_spells]
	m.library.add(spells)

	map(m.core.connect, rubies)
	players.append(m)

	l = ManaEater(owner=m, hook_db=hook_db, position=m.core)
	m.add_creature(l)
	m.core.add_creature(l)

	m.focus()

	return m

players = []
