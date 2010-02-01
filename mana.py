#!/usr/bin/env python
from seed import players,spells,create_player,hook_db
from ui import UI

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

	player.focus()
	ui.active = False
