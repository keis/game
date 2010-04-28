from error import GameError, IllegalMovement
from owned import friendly
from xselect import select
from seed import context,ids

#TODO:
# legal moves: s/leaf/node with free pad/
# from friendly non-leaf to any friendly node
# from friendly leaf to friendly non-leaf
# from friendly leaf to opposing leaf if not engaged in battle
# from opposing leaf to friendly leaf

def move_creatures(player, creatures, building):
	""" Move all of @creatures to @building."""

	if any(getattr(c, 'owner', None) != player):
		raise IllegalMovement("Player does control all creatues")

	is_attack = not friendly(building, creatures[0])

	# To move to a opposing building a free pad is required
	if is_attack and not len(building.free_pads()) > 0:
		raise IllegalMovement("No free pads")

	# Should the entire movement be aborted if one creature fails its pre-move check?
	creatures = [x for x in creatures if x.run_hook('pre-move', building)[0]]
	creatures = filter(None, map(lambda x: x.position.remove_creature(x), creatures))
	creatures = filter(None, map(lambda x: building.add_creature(x), creatures))

	for x in creatures:
		x.position = building


def cast_spell(player, spell, targets):
	if spell not in player.focused:
		raise GameError("Spell not focused")

	tmp = {
		'self' : player,
		'opponent' : None
	}
	tmp.update(ids)

	for k,v in targets.items():
		try:
			help, dv = spell._desc[k]
		except KeyError:
			raise GameError("Unknown target name (%s)" % k)

		if v not in select(dv, context, IDs = tmp):
			raise GameError("Illegal target %s" % v)

	player.cast_spell(spell, targets)
