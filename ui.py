from seed import players,spells,buildings,creatures,hook_db
from textview import db as view_db
from error import GameError

class UI(object):
	aliases = {
		'players' : '#root > Mage',
		'all_spells' : 'Enabled > SpellMeta',
		'all_buildings' : 'Enabled > BuildingMeta',
		'all_creatures' : 'Enabled > CreatureMeta',
		'base' : '#self > Summary > Building',
		'buildings' : '#self > Summary > Building',
		'focused' : '#self Focused *',
		'library' : '#self Library *',
		'op_base' : '#opponent > Summary > Building',
		'op_buildings' : '#opponent > Summary > Building',
		'creatures' : '#self > Summary > Creature',
		'op_creatures' : '#opponent > Summary > Creature',
	}

	def __init__(self, player):
		self.player = player
		self.active = False

		hook_db.hook(None, 'post-repair', self.repair_p)
		hook_db.hook(None, 'post-heal', self.heal_p)
		hook_db.hook(None, 'post-discard', self.discard_p)
		hook_db.hook(None, 'post-add-damage', self.add_damage_p)
		hook_db.hook(None, 'post-destroy', self.destroy_p)
		hook_db.hook(None, 'post-stealth', self.stealth_p)

	def repair_p(self, target, source, amount):
		if self.active:
			print "%s was repaired for %s by %s" % (self.view(target), amount, self.view(source))

	def heal_p(self, target, source, amount):
		if self.active:
			print "%s was healed for %s by %s" % (self.view(target), amount, self.view(source))

	def add_damage_p(self, target, amount):
		if self.active:
			print "%s was dealt %s damage" % (self.view(target), amount)

	def discard_p(self, target):
		if self.active:
			print "%s was discarded" % self.view(target)

	def destroy_p(self, target):
		if self.active:
			print "%s was destroyed" % self.view(target)

	def stealth_p(self, target):
		if self.active:
			print "%s fades into the shadows" % self.view(target)

	def view(self, obj, **kwargs):
		return view_db[obj](self.player, obj, **kwargs)

	def _select(self, q, c=None):
		from xselect import _select
		if c is None:
			c = self.player.context

		tmp = self.player.build_IDs()
		
		return _select(q, c, IDs = tmp)
	
	def select(self, q , c=None):
		from xselect import select
		if c is None:
			c = self.player.context

		tmp = self.player.build_IDs()
		
		return select(q, c, IDs = tmp)

	def select_targets(self, spell):
		desc = spell._desc
		targets = {}
		for k,(v,s) in desc.items():
			print '%s (%s):' % (k,v)
			if s is None:
				p = stuff
			print 'select', s
			p = self.select(s)
			print self.view(p, enumerate=True, newline_sep=True)

			while True:
				input = raw_input()
				if input[0] == '?':
					print self.view(p[int(input[1:])], long=True)
				else:
					target = p[int(input)]
					break
				
			targets[k] = target
		return targets

	def cmd_cast(self, what):
		try:
			x = int(what)
			spell = self.player.focused_spells()[x]
		except IndexError:
			print "There is no such spell"
			return
		except ValueError:
			# if it's not a number, maybe it was the spell name
			for x in self.player.focused_spells():
				if x._name == what:
					spell = x
					break
			else:
				print "I Don't know what spell you want to cast, use e.g 'cast 2' or 'cast summon'"
				return

		targets = self.select_targets(spell)

		try: self.player.cast_spell(spell, targets)
		except GameError, e:
			print "Oh No! you made the game sad"
			print "\t%s - %s" % (type(e), e)
			return

	def cmd_show(self, what='focused', index=None):
		what = self.aliases.get(what, what) # in da butt

		try: things = self.select(what)
		except KeyError:
			print "Show me yours first"
			return

		if index is None:
			print self.view(things, enumerate=True, newline_sep=True)
		else:
			try:
				obj = things[int(index)]
			except ValueError:
				print "That's not a valid name"
				return
			except IndexError:
				print "There is no such thing"
				return

			print self.view(obj, long=True)

	def cmd_select(self, *args):
		objs = self._select(args)
		print self.view(objs)

	def cmd_move(self, *args):
		try: pivot = args.index('to')
		except ValueError:
			print "you are missing a 'to' there"
			return

		target = args[pivot+1].split('-')

		try:
			if len(target) == 2:
				all_buildings = self.select(self.aliases['%s_buildings' % target[0]])
				target = int(target[1])
			else:
				all_buildings = self.select(self.aliases['buildings'])
				target = int(target[0])
			target = all_buildings[target]
		except ValueError:
			print "That's not a valid building name"
			return
		except IndexError:
			print "There is no such building"
			print self.view(all_buildings)
			return
			
		all_units = self.select(self.aliases['creatures'])

		try: units = map(lambda x: all_units[int(x)], args[:pivot])
		except ValueError:
			print "That's not a valid unit name"
			return
		except IndexError:
			print "There is no such unit"
			return

		if len(units) == 0:
			print "You don't want to move anything? fine with me"
			return

		try: self.player.order_movement(units, target)
		except GameError, e:
			print "Oh No! you made the game sad"
			print "\t%s - %s" % (type(e), e)
			return

	def cmd_done(self):
		return False

	def short_spell_list(self):
		spells = self.player.focused_spells()
		return ', '.join(['%d) %s (%s)' % (i, x._name, x._cost) for i,x in enumerate(spells)])

	def input(self):
		cmds = {'cast':self.cmd_cast, 'show':self.cmd_show, 'move':self.cmd_move, 'select':self.cmd_select, 'done':self.cmd_done}
		print 'mana:', self.player.mana
		print self.short_spell_list()
		data = raw_input(">").split(' ')
		try:
			cmd = cmds[data[0]]
		except KeyError:
			return
		return cmd(*data[1:])
