from view import View,ViewDB
from building import Building
from creature import Creature
from spell import Spell
from mage import Mage
from zone import zHidden,zPrivate,zPublic

import buildings

def view(viewer, obj, **kwargs):
	return db[obj](viewer, obj, **kwargs)

class BuildingView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		inner = ''
		if opts.get('tree', False):
			inner = str(view(viewer, obj.pads, **opts))
		return '<Building type="%s">%s</Building>' % (obj.__class__.__name__, inner)

class CreatureView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		return '<Creature type="%s" atk="%s def="%s" damage="%s" hp="%s"/>' % (obj.__class__.__name__, obj.get_attack(), obj.get_defence(), obj.damage, obj.hp)

class SpellView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		return '<Spell name="%s" cost="%s"/>' % (obj._name, obj._cost)

class ManaShardView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		return '<ManaShard capacity="%s"/>' % obj.capacity

class MageView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		return '<Mage name="%s"/>' % obj.name

class ListView(View):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		subviews = [view(viewer, x, **opts) for x in obj]
		return ''.join([str(x) for x in subviews])

class ZoneView(ListView):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		return '<Zone name="%s">%s</Zone>' % (obj._name, super(ZoneView, self).__str__())

class HiddenZoneView(ZoneView):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts

		return '<Zone name="%s">This information is not for your eyes</Zone>' % obj._name

class PrivateZoneView(ZoneView):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		if viewer == obj.owner:
			return super(PrivateZoneView, self).__str__()
		return '<Zone name="%s">This information is private</Zone>' % obj._name

class PublicZoneView(ZoneView):
	def __str__(self):
		viewer,obj,opts = self.viewer,self.obj,self.opts
		return super(PublicZoneView, self).__str__()

db = ViewDB()
db.update({
	tuple : ListView,
	list : ListView,
	Building : BuildingView,
	Creature : CreatureView,
	Mage : MageView,
	Spell : SpellView,
	zHidden : HiddenZoneView,
	zPrivate : PrivateZoneView,
	zPublic : PublicZoneView,
	buildings.ManaRuby.ManaShard : ManaShardView
})
