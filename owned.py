from hook import Hookable

class Owned(Hookable):
	def __init__(self, owner=None, **kwargs):
		# A little trick to avoid passing around hook_db 
		if 'hook_db' not in kwargs and owner is not None:
			kwargs['hook_db'] = owner._hook_db

		super(Owned, self).__init__(**kwargs)
		self.owner = owner

	def claim(self, owner):
		(owner,) = self.run_hook('pre-claim', owner)
		if owner is not None:
			self.owner = owner
			self.run_hook('post-claim', owner)

def friendly(a,b):
	return getattr(a, 'owner', None) == getattr(b, 'owner', None)
