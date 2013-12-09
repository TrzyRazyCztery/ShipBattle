from Ship import Ship
from random import randint,choice

class Game():
	def __init__(self):
		"""
		w configu na pierwszym miejscu jest krotka z wielkoscia planszy
		dlatego odwołuje sie do [0][0].
		"""

		self._config = self.__openConfig()
		self._map = self.__mapCreator(eval(self._config[0][0]))
		self.shipList = self.shipPositioning()
		#self.listaStatkow=[self.__addingShip(self._config[x],(4,5),"h") for x in range(1,len(self._config))] 
	def __openConfig(self):
		"""
		otwiera plik konfiguracyjny ktory zawiera w pierwszej linijce rozmiary mapy a w reszcie linni
		nazwy statkow i ich wielkosc
		"""
		return [x[:-1].split(" ") for x in open('config.txt', 'r')]
		

	def __mapCreator(self,size):
		"""
		Tworzy mapę o podanych rozmiarach
		"""	 
		return [[" " for x in range(size[0])] for y in range(size[1]) ]

	def __addingShip(self,config,position,direction,name):
		"""
		podajac linijke z pliku konfiguracyjnego postaci (Nazwa liczba) pozycje i polozenie
		tworzy nowy obiekt statek o w/w parametrach
		"""
		globals()[config[0]] = eval("Ship(position,direction,"+config[1]+","+"config[0]"+ ")")
		return(eval(config[0]))

	def isFinished(self):
		"""
		sprawdzamy czy gra sie nie zakończyła
		"""
		for ship in self.shipList:
			if (ship.isDestroyed() == False):
				return False
		return True

	def game(self):
		"""
		Główna pętla gry wywołuje sie do czasu gdy wszystkie statki beda rozbite
		"""
		counter = 0
		while not self.isFinished():
			counter += 1	
			position = input("write coordinates (like A7)  : ")
			alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" ")
			try:
				self.turn((int(alphabet.index(position[0])),int(position[1:])))
			except:
				print("index must be in map")
		print("Congratulations, you finished in",counter,"moves")


	def turn(self,coordinates):
		"""
		sterowanie tura
		"""
		print(coordinates)
		self.shoot(coordinates)
		self.printMap()

				
	def shoot(self,position):
		"""
		funkcja zwraca trafienie z nazwa i dlugoscia jesli nasz punkt jest czescia jakiegos statku
		i oznacza to miejsce na mapie O jesli ie trafimy jest X
		"""
		for ship in self.shipList:
			if (ship.tryShoot(position)):
				ship.shoot(position)
				print ("You shot in",ship.name," size: ",ship.length)
				self._map[position[1]][position[0]] = "O"
				if (ship.isDestroyed()):
					print("sunken")
				return True
		print(position[1],position[0])		
		self._map[position[1]][position[0]] = "X"
		print("miss")
		return False		

	def printMap(self):
		alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" ")
		print("X",alphabet[:len(self._map)])
		for i in range(1, len(self._map)+1):
			print (i-1,self._map[i-1])

	def shipPositioning(self):
		"""
		z pliku konfiguracyjnego pobiera statki losowo umieszcza je na mapie zwracajac liste obiektów typu "Ship"
		z przypisanymi wspolrzednymi, innym slowem gotowa lista złożona ze statkow umiejscowionych na mapie
		"""
		shipList = []
		trash = {}#zajete pozycje
		for i in range(1,len(self._config)):#wykonuje się tyle razy ile wymaga tego plik konfiguracyjny
			onMap = True #while wykonuje sie dopoty dopóki nie uda mu sie umieścić statku na planszy
			size = int(self._config[i][1]) #rozmiar pobiera z pliku konfiguracyjnego
			while onMap:
				direction = choice(["v","h"]) #losuje czy statek ustawić pionowo czy poziomo (horizontal or vertical)
				stop=0 #warunek przerwania pętli w razie kolizji statków
				if (direction == "h"):
					x = randint(0,len(self._map[0])-size) #dla poziomych x losujemy z puli zmniejszonej o rozmiar satku żeby nie wyjechac za mape
					y = randint(0,len(self._map)-1) #minus 1 bo randint losuje z domkmnieciem przedzialu a ostatni indeks jest mniejszy niż wielkosc listy (indeksowanie od 0)
					for j in range(size):
						if (trash.get((x+j,y),False) == True): 
							stop = 1 # sprawdzamy czy nasze x,y kore wylosowalismy dla statku nie sa juz zajete
							break # jesli sa to przerywam sprawdzanie dalej i warunek stopu ustawiam na 1
					if (stop == 0): #jelsi nie dostalismy warunku stopu to  oznaczamy że nasz statek juz ma swoje punkty na mapie zeby przerwac while		
						onMap = False
						for j in range(1,-2,-1): # do naszego smietniczka z zajetymi pozycjamy dorzucamy też obramowanie staku co pozwoli uniknąć kolizji
							for k in range(size+2):
								trash[(x-1+k,y+j)] = True	

				else:  #tutaj to samo co dla poziomych tylko zmieniamy y
					x = randint(0,len(self._map[0])-1)
					y = randint(0,len(self._map)-size)	
					for k in range(size):
						if (trash.get((x,y+k),False) == True):
							stop=1
							break
					if (stop==0):			
						onMap = False
						for j in range(1,-2,-1):
							for k in range(size+2):
								trash[(x+j,y-1+k)] = True
							
			shipList.append(self.__addingShip(self._config[i],(x,y),direction,self._config[i][0]))						
		return shipList		

a = Game()

a.game()
