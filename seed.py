from mage import Mage
from spell import Spell, prepare_spell, focus_spell, magic_arrow, repair, summon, construct
from buildings import SmallManaRuby,MediumManaRuby,LargeManaRuby,Core,Boulder
from creatures import LizardDemon, Skeleton, Adventurer, Summoner
from hook import HookDB

spells = (prepare_spell, magic_arrow, focus_spell, repair, summon, construct)
creatures = (LizardDemon, Skeleton, Adventurer, Summoner)
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
	spells = [x(owner=m) for x in starting_spells]
	m.library.add(spells)

	map(m.core.connect, rubies)
	m.focus()
	players.append(m)

	l = LizardDemon(owner=m, hook_db=hook_db, position=m.core)
	m.creatures.append(l)
	m.core.add_creature(l)

	return m

players = []
