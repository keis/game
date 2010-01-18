import random
from owned import Owned

class Zone(Owned, list):
	def __init__(self, name=None, **kwargs):
		super(Zone, self).__init__(**kwargs)
		self._name = name

	def clear(self):
		self[:] = []

	def get(self, cnt=1):
		self.prepare()
		r,self[:] = self[:cnt],self[cnt:]
		return r

	def add(self, item):
		try:
			self.extend(item[:])
		except TypeError:
			self.append(item)

class zHidden(Zone): pass
class zPrivate(Zone): pass
class zPublic(Zone): pass

class zUnordered(Zone):
	def prepare(self):
		pass

class zSorted(Zone):
	def prepare(self):
		pass

class zRandom(Zone):
	def prepare(self):
		random.shuffle(self)
