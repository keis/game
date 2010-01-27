from zone import zUnordered,zPublic
from owned import Owned

class Channeler(Owned):
	""" Base class for objects adding items to its owners POOL """
	zone_type = type('channeler_zone', (zUnordered, zPublic), {})

	def __init__(self, **kwargs):
		super(Channeler, self).__init__(**kwargs)
		self._zone = self.zone_type(owner=self.owner)
		self.owner.add_hook('pre-build-pool', lambda z: z.add(self._zone))

	def add(self, focusable):
		self._zone.add(focusable)
