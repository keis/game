from owned import Owned

class Focusable(Owned):
	def __init__(self, tags = (), **kwargs):
		super(Focusable, self).__init__(**kwargs)
		self.owner.library.add(self)
		self.tags = tags

	def focus(self):
		self.owner.library.remove(self)
		self.owner.focused.add(self)

	def unfocus(self):
		self.owner.focused.remove(self)
		self.owner.library.add(self)

	def discard(self):
		# should have diffrent triggers
		self.unfocus()
