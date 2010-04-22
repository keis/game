from view import View,ViewDB
from building import Building
from creature import Creature
from zone import zHidden,zPrivate,zPublic

def view(viewer, obj, **kwargs):
	return db[obj](viewer, obj, **kwargs)

class BuildingView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		if not opts.get('long', False):
			return str(obj.__class__.__name__)
		return """%s (%s/%s)
Connected To: %s
Units: %s""" % (obj.__class__.__name__, obj.damage, obj.hp, view(viewer, obj.parent), view(viewer, obj.units))

class CreatureView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		if obj.stealthed and getattr(obj, 'owner', None) != self.viewer:
			return ''
		if not opts.get('long', False):
			return str(obj.__class__.__name__)
		return """%s at %s
Attack: %d
Defence: %d
Damage/HP: %d/%d""" % (obj.__class__.__name__, view(viewer, obj.position),  obj.get_attack(), obj.get_defence(), obj.damage, obj.hp)

class ListView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		sep = ', '
		subviews = [view(viewer, x) for x in obj]
		if opts.get('enumerate', False):
			subviews = ['%d) %s' % (i,x) for i,x in enumerate(subviews)]
		if opts.get('newline_sep', False):
			sep = '\n'
		return sep.join([str(x) for x in subviews])

class HiddenZoneView(ListView):
	def __str__(self):
		return "This information is not for your eyes"

class PrivateZoneView(ListView):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		if viewer == obj.owner:
			return super(PrivateZoneView, self).__str__()
		return "This information is private"

class PublicZoneView(ListView):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		return super(PublicZoneView, self).__str__()

db = ViewDB()
db.update({
	tuple : ListView,
	list : ListView,
	Building : BuildingView,
	Creature : CreatureView,
	zHidden : HiddenZoneView,
	zPrivate : PrivateZoneView,
	zPublic : PublicZoneView
})
