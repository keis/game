from building import Building
from owned import Owned
from focusable import Focusable
import effects

class Core(Building, Owned):
	npads = 3
	hp = 6000
	def __init__(self, **kwargs):
		super(Core, self).__init__(**kwargs)
		def start_hook(t, player):
			if player == self.owner:
				effects.repair(self,self)
				effects.heal(self,self)

		def destroy_hook():
			print 'STUB: core destroy_hook'
			raise Exception("%s has lost the game" % self.owner)

		self.add_global_hook('start-of-turn', start_hook)
		self.add_hook('post-destroy', destroy_hook)

class ManaRuby(Building, Owned):
	npads = 2

	class ManaShard(Focusable):
		def __init__(self, capacity=None, **kwargs):
			self.capacity = capacity
			super(ManaRuby.ManaShard, self).__init__(**kwargs)

		def __str__(self):
			return "mana shard (%d)" % self.capacity

	def __init__(self, **kwargs):
		super(ManaRuby, self).__init__(**kwargs)

		self._shards = [ManaRuby.ManaShard(capacity=self.shard_size, owner=self.owner) for x in range(self.shard_count)]
		self.add_hook('pre-repair', lambda s, a: (s, a * 1.5) )
		self.owner.add_hook('pre-build-pool', lambda z: z.add(self._shards))

class SmallManaRuby(ManaRuby):
	shard_count = 1
	shard_size = 5
	hp = 2000

class MediumManaRuby(ManaRuby):
	shard_count = 2
	shard_size = 8
	hp = 2000
	cost = 2

class LargeManaRuby(ManaRuby):
	shard_count = 3
	shard_size = 10
	hp = 2000
	cost = 4

class Boulder(Building, Focusable):
	npads = 1
	hp = 8000
	cost = 1

	def __init__(self, **kwargs):
		super(Boulder, self).__init__(**kwargs)

		self.add_hook('pre-repair', lambda s, a: (s, 0))
		self.owner.add_hook('pre-build-pool', lambda z: z.add(self))
