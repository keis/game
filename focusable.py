from owned import Owned
from hook import Hookable
from error import AlreadyFocusedError,NotFocusedError

class Focusable(Owned, Hookable):
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
		self.run_hook('pre-discard')
		self.unfocus()
		self.run_hook('post-discard')
