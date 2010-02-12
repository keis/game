class View(object):
	def __init__(self, viewer, obj, **kwargs):
		self.viewer, self.obj, self.opts = viewer, obj, kwargs

	def __str__(self):
		return str(self.obj)

##
# builds a list of all classes in a inheritance tree using the same ordering as name lookup in python
def classes(cls):
	list = [cls]
	for cls in list:
		list.extend([base for base in cls.__bases__ if base not in list])

	return list

class ViewDB(dict):
	def __getitem__(self, obj):
		try:
			return dict.__getitem__(self, obj)
		except (KeyError,TypeError):
			# TypeError is for "unhashable type"
			for x in classes(obj.__class__):
				try:
					return dict.__getitem__(self, x)
				except KeyError: pass
		return View
