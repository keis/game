from error import IllegalMovement
from owned import friendly

# TODO, come up with a real battle system
# * defence bonus from buildings
# * attack/defence bonus depending on enemies/allies
# * armour? damage soakers? user ctrl damage dealing?
# * also, hooks!

def deal_damage(units, amount):
	for x in units:
		target = min(x.hp - x.damage, amount)
		x.add_damage(target)
		amount -= target
		if amount == 0:
			break
	return amount

def battle(attackers, building):
	defenders = building.get_defenders()
	
	a = reduce(lambda s,d: s + d.get_attack(), attackers, 0)
	d = reduce(lambda s,d: s + d.get_defence(), defenders, 0)

	arest = deal_damage(defenders, a)
	drest = deal_damage(attackers, d)

	building.add_damage(arest)
	# do something with drest?

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

	if is_attack:
		battle(creatures, building)
