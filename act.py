from error import IllegalMovement
from owned import friendly

MASSACRE_THRESHOLD = 300.0

# TODO, come up with a real battle system
# * defence bonus from buildings
# * attack/defence bonus depending on enemies/allies
# * armour? damage soakers? user ctrl damage dealing?
# * also, hooks!

def deal_damage(units, amount):
	units.sort(key=lambda x: -x.hp)

	for x in units:
		target = min(x.hp - x.damage, amount)
		x.add_damage(target)
		amount -= target
		if amount == 0:
			break
	return amount

def battle(building):
	def damage_scale(x):
		return 2 ** (x/MASSACRE_THRESHOLD)

	defenders = building.get_defenders()
	attackers = building.get_attackers()

	a = sum([x.get_attack() for x in attackers])
	d = sum([x.get_defence() for x in defenders])

	ascale = damage_scale(a - d - building.get_defence_bonus())
	dscale = damage_scale(d - a)

	arest = deal_damage(defenders, a * ascale)
	drest = deal_damage(attackers, d * dscale)

	building.add_damage(arest)
	# do something with drest?

#TODO:
# legal moves: s/leaf/node with free pad/
# from friendly non-leaf to any friendly node
# from friendly leaf to friendly non-leaf
# from friendly leaf to opposing leaf if not engaged in battle
# from opposing leaf to friendly leaf

def move_creatures(creatures, building):
	""" Move all of @creatures to @building. it is required that all units share owner """

	is_attack = not friendly(building, creatures[0])

	# To move to a opposing building a free pad is required
	if is_attack and not len(building.free_pads()) > 0:
		raise IllegalMovement("No free pads")

	creatures = [x for x in creatures if x.run_hook('pre-move', building)[0]]
	creatures = filter(None, map(lambda x: x.position.remove_creature(x), creatures))
	creatures = filter(None, map(lambda x: building.add_creature(x), creatures))

	for x in creatures:
		x.position = building
