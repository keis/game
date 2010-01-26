from owned import Owned
from error import AlreadyFocusedError,NotFocusedError

class Focusable(Owned):
	def __init__(self, tags = (), **kwargs):
		super(Focusable, self).__init__(**kwargs)
		self.tags = tags

	def focus(self):
		if self in self.owner.focused:
			raise AlreadyFocusedError()
		self.owner.focused.add(self)

	def unfocus(self):
		if self not in self.owner.focused:
			raise NotFocusedError()
		self.owner.focused.remove(self)

	def discard(self):
		# should have diffrent triggers
		self.unfocus()
