# Some standard effects used by spells and other stuff

def repair(source, building):
	def _repair(b, power):
		b.repair(source, power)
	building.apply_aoe(_repair, lambda c,x: x * 0.8, 100)


def heal(source, building):
	def _heal(b, power):
		b.heal(source, power)
	building.apply_aoe(_heal, lambda c,x: x * 0.8, 100)

def charge(source, frm, to, scale=1.5):
	power = {'value':0}
	def _charge(b, p):
		power['value'] += p
	frm.apply_line(to, _charge, lambda c,x: x * scale, 100)
	return power['value']
