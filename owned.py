
class Owned(object):
	def __init__(self, owner=None, **kwargs):
		super(Owned, self).__init__(**kwargs)
		self.owner = owner

	def claim(self, owner):
		if self.owner == None:
			self.owner = owner
		else:
			pass
			# some fancy logic
