class Ship():

	def __init__ (self,position,direction,length,name):
		'''
		position - pozycja, krtka x,y
		direction - kierunek h dla horizontal (poziom) v dla veritcal (pion)
		length - dlugosc statku
		'''
		self.name = name
		self.length = length
		self.direction = direction
		self.x = position[0]
		self.y = position[1]
		if (self.direction == "v"):
			self._positions = [ (self.x, self.y+i) for i in range(self.length)]
		if 	(self.direction == "h"):
			self._positions = [ (self.x+i, self.y) for i in range(self.length)]

		self.hit = {}

	def positions(self):
		return self._positions

	def isDestroyed(self):
		"""
		Czy statek jest zniszczony, porównuje liste krotek statku z 
		lista trafionych krotek)
		"""
		for position in self._positions:
			if not (self.hit.get(position,False)):
				return False
		return True
	
	def tryShoot(self,position):
		"""
		jesli na danej pozycji jest nasz statek i nikt w niego jeszcze nikt
		w niego nie trafił zwracamy True w innych przypadkach False
		"""
		if (position in self._positions and not self.hit.get(position,False)):
			return True
		elif (position not in self._positions or self.hit.get(position,False)):
			return False
	
	def shoot(self,position):
		"""
		oddaje strzal do naszego statku, jelsi trafil kapitan zwraca True 
		jesli nie False
		"""	
		if (self.tryShoot(position)):
			self.hit[position] = True
			return True
		else:
			return False


