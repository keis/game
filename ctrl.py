import seed

class Ctrl(object):
	def __init__(self):

		self.players = []

	def add_player(self, name):
		p = seed.create_player()
		self.players.append((name,p))

	def start(self):
		def turns():
			while True:
				for p in self.players:
					yield p
		self.turns = turns()
		
