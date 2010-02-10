from hook import Hookable
from creature import CreatureStack
from owned import friendly

class Tree(object):
	npads = 1
	def __init__(self, **kwargs):
		super(Tree, self).__init__(**kwargs)
		self.parent = None
		self.pads = [None] * self.npads

	def connect(self, other, index = 0):
		# index have only a estetical effect, but I like to feel pretty
		pads = self.free_pads()
		if other.parent is None and pads:
			src,sindex = pads[index]
			src.pads[sindex] = other
			other.parent = self

	def free_pads(self):
		return [(self,i) for i,x in enumerate(self.pads) if x is None]

	def network(self):
		yield self
		for x in self.pads:
			if x is not None:
				for y in x.network():
					yield y

	def network_free_pads(self):
		return reduce(lambda pads,building: pads + building.free_pads(), self.network(), [])

	def find(self, other):
		try:
			i = self.pads.index(other)
			return [i]
		except ValueError:
			for (i,x) in enumerate(self.pads):
				if x is not None:
					path = x.find(other)
					if path:
						return [i] + path
		return None

	def dft_fold(self, func, initial = 0):
		v = func(self, initial)
		children = [x for x in self.pads if x is not None]
		return map(lambda x: x.dft_fold(func, v), children)

	def _cleanup(self):
		try: cleanup = super(Tree, self)._cleanup
		except AttributeError: pass
		else: cleanup()

		self.parent.pads = [x if x != self else None for x in self.parent.pads]

# This class makes sure pretty printing of building-classes is done
class BuildingMeta(type):
	def __str__(self):
		return '%s (%d/%d) %d' % (self.__name__, self.npads, self.hp, self.cost)

class Building(Tree, Hookable):
	__metaclass__ = BuildingMeta
	hp = 100
	defence = 10
	cost = 1
	def __init__(self, damage = 0, **kwargs):
		super(Building, self).__init__(**kwargs)
		self.damage = damage
		self.units = CreatureStack()

	def apply_aoe(self, f, power_f, power):
		def _apply_aoe(current, power):
			f(current, power)
			power = power_f(current, power)
			(power,) = current.run_hook('pre-aoe-scale', power)
			current.run_hook('post-aoe-scale', power)
			return power

		self.dft_fold(_apply_aoe, power)

	def apply_line(self, target, f, power_f, power):
		def apply_path(current, path, power):
			f(current, power)
			power = power_f(current, power)
			(power,) = current.run_hook('pre-line-scale', power)
			current.run_hook('post-line-scale', power)
			apply_path(current.pads[path[0]], path[1:], power)
			
		path = self.find(target)
		apply_path(self, path, power)

	def add_damage(self, amount):
		self.damage += amount
		if self.damage >= self.hp:
			self.destroy()

	def destroy(self):
		# the exact actions taken here is subject to change!
		self.run_hook('pre-destroy')

		# destroy all child nodes
		for x in self.pads:
			if x is not None:
				x.destroy()

		if hasattr(self, 'owner'):
			self.owner.remove_building(self)

		print '%s was destroyed' % self
		self.run_hook('post-destroy')

		# move all units to parent (bypassing normal movement rules)
		# This will emit alot of add-creature. dunno if that is wanted
		for x in self.units:
			x.position = self.parent
			self.parent.add_creature(x)

		self._cleanup()

		print list(self.parent.network())

	def remove_creature(self, creature):
		(creature,) = self.run_hook('pre-remove-creature', creature)
		if creature:
			self.units.remove(creature)
			self.run_hook('post-remove-creature', creature)
		return creature

	def add_creature(self, creature):
		(creature,) = self.run_hook('pre-add-creature', creature)
		if creature:
			self.units.append(creature)
			self.run_hook('post-add-creature', creature)
		return creature

	def repair(self, source, amount):
		source, amount = self.run_hook('pre-repair', source, amount)
		if source and amount:
			self.damage = max(self.damage - amount, 0)
			self.run_hook('post-repair', source, amount)
		return source, amount

	def heal(self, source, amount):
		#source, amount = self.run_hook('pre-heal', source, amount)
		if source and amount:
			for x in self.units:
				if friendly(self, x):
					x.heal(source, amount)
		#	self.run_hook('post-heal', source, amount)
		return source, amount

	def get_defence_bonus(self):
		return self.defence

	def get_defenders(self):
		# Maybe allow some teleport dude to defend at all buildings..
		defenders = [x for x in self.units if friendly(self, x)]
		(defenders,) = self.run_hook('pre-defenders', defenders)
		self.run_hook('post-defenders', defenders)
		return defenders

	def get_attackers(self):
		attackers = [x for x in self.units if not friendly(self, x)]
		(attackers,) = self.run_hook('pre-attackers', attackers)
		self.run_hook('post-attackers', attackers)
		return attackers

	def is_battle_zone(self):
		return any(not friendly(self, x) for x in self.units)

	def _cleanup(self):
		try: cleanup = super(Building, self)._cleanup
		except AttributeError: pass
		else: cleanup()

		self.units[:] = []
