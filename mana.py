#!/usr/bin/env python
from seed import players,spells,create_player,hook_db
from ui import UI
import act

for x in range(2):
	create_player()

uis = [UI(players[0], players[1]), UI(players[1], players[0])]

def turns():
	while True:
		for p,u in zip(players,uis):
			yield p,u
turns = turns()

for t in turns:
	player,ui = t
	ui.active = True
	print "it is now %s's turn" % player
	hook_db.run_hook(None, 'start-of-turn', player)

	while ui.input() != False: pass

	for p in players:
		battles = [x for x in p.core.network() if x.is_battle_zone()]
		if len(battles) > 0:
			for x in battles:
				print 'battle @ %s' % x
				act.battle(x)
		else:
			print "no battles in %s territory" % p

	player.focus()
	ui.active = False
