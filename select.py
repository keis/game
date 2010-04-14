#!/usr/bin/env python
import re

def flatten(tree):
	for x in tree:
		yield x
		try:
			if not isinstance(x, basestring):
				i = flatten(x)
				for y in i:
					yield y
		except TypeError:
			pass

robj = re.compile(r'([a-zA-Z]*)(\[([a-zA-Z]+=.+)\])?')
def _select(q, context):
	def children(x):
		try: iter(x)
		except TypeError:
			return []
		return list(x)

	def dodesc(x):
		return reduce(lambda a,o: a + list(flatten(children(o))), x, [])

	def matchtype(x, t):
		if x.__name__ == t:
			return True

		for b in x.__bases__:
			if matchtype(b, t):
				return True

		return False

	def matchattr(x, (key, value)):
		return str(getattr(x, key, None)) == value
		
	out = flatten(context)
	descNext = False
	for x in q:
		desc = descNext
		descNext = False
		if x in ('*',''):
			if desc:
				out = dodesc(out)
		elif x == '>':
			print len(out)
			out = reduce(lambda a,o: a + children(o), out, [])
		else:
			if desc:
				out = dodesc(out)
			t,attr = robj.match(x).group(1,3)
			out = filter(lambda o: (not t or matchtype(type(o), t)) and (not attr or matchattr(o, attr.split('='))), out)
			descNext = True
	return list(out)

def select(q, context):
	return _select(q.split(' '), context)

if __name__ == '__main__':
	def dump(d):
		print ', '.join([str(type(x)) for x in d])

	class Foo(list):
		pass

	class Bar(list):
		pass

	class Bark(Bar):
		pass

	root = [Foo([Bar(),Bar(),Bark([Bark()])]), Bar([Bar([Bark()])])]

	select('Bark', root)[1].foo = '^^'

	#dump(select('', root))
	#dump(select('>', root))
	dump(select('[foo=^^]', root))
	#dump(select('*', root))
	#dump(select('Bar', root))
	#dump(select('Bar > Bark', root))
	#dump(select('Bar > *', root))
	#dump(select('Bar Bar', root))
	#dump(select('Foo *', root))
