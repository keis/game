from functools import partial
from collections import defaultdict

class Hookable(object):
	def __init__(self, hook_db = None, **kwargs):
		self._hook_db = hook_db
		super(Hookable, self).__init__(**kwargs)

	def __hook(self, obj, key, func, *bargs, **kwargs):
		func = partial(func, *bargs)
		self._hook_db.hook(obj, key, func, owner=kwargs.get('owner', self))

	def add_hook(self, *args, **kwargs):
		self.__hook(self, *args, **kwargs)

	def add_global_hook(self, *args, **kwargs):
		self.__hook(None, *args, **kwargs)

	def clear_hooks(self):
		if self in self._hook_db:
			del self._hook_db[self]

	def run_hook(self, key, *args):
		return self._hook_db.run_hook(self, key, *args)

	def _cleanup(self):
		try: cleanup = super(Hookable, self)._cleanup
		except AttributeError: pass
		else: cleanup()

		self.clear_hooks()
		self._hook_db.clear_owned_hooks(self)

def hook_caller(f, *args):
	_args = f(*args)

	if _args is None:
		return args

	if len(args) == 1:
		_args = (_args,)

	return _args

def global_hook_caller(f, target, *args):
	_args = f(target, *args)

	if _args is None:
		return args

	if len(args) == 1:
		_args = (_args,)

	return _args

# to simplify the cleanup of objects consider adding a 'controller' of a hook
# and a way to clean all hooks with a given controller
class HookDB(defaultdict):
	""" A database where each (Object,hook-string) gives a list of hooks to run.
	the use of None as Object is treated as a hook to be applied to all objects and
	can also be used to hook events not tied to a object."""
	hook_dict = partial(defaultdict, list)
	def __init__(self):
		defaultdict.__init__(self, HookDB.hook_dict)

	def hook(self, target, key, func, owner=None):
		if owner is None:
			owner = target

		if owner is not None:
			try:
				owner.__hooks
			except AttributeError:
				owner.__hooks = []
			owner.__hooks.append((target,key))
		self[target][key].append((func, owner))

	# Clear all hooks matching target, key and owner (which defaults to target)
	def clear_hook(self, target, key, owner=None):
		owner = owner or target
		hooks = [(f,o) for f,o in self.get_hooks(target, key) if o != owner]
		self[target][key] = hooks

	def clear_owned_hooks(self, owner):
		try:
			hooks = owner.__hooks
		except AttributeError:
			return

		for t,k in hooks:
			self.clear_hook(t, k, owner)

		owner.__hooks = []
			
	def get_hooks(self, target, key):
		# use get to avoid creating lots of empty lists in the db
		return self.get(target, {}).get(key, [])

	def __run_global_hook(self, target, key, *args):
		"""Runs all global hooks for @key (hooked to None). callbacks should take
		an additional first argument that is the subject which should NOT be returned."""
		for f,o in self.get_hooks(None, key):
			args = global_hook_caller(f, target, *args)
		return args

	def run_hook(self, target, key, *args):
		"""Runs all hooks for @key on @target, callbacks should return the arguments which is allowed
		to be modified or return None."""
		#print 'run_hook', target, key
		if target is None:
			return self.__run_global_hook(None, key, *args)

		for f,o in self.get_hooks(target, key):
			args = hook_caller(f, *args)

		# Run global hooks too
		args = hook_caller(self.__run_global_hook, target, key, *args)

		return args
