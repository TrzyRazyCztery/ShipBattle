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

	def __addingShip(self,config,position,direction):
		"""
		podajac linijke z pliku konfiguracyjnego postaci (Nazwa liczba) pozycje i polozenie
		tworzy nowy obiekt statek o w/w parametrach
		"""
		globals()[config[0]] = eval("Ship(position,direction,"+config[1]+")")
		return(eval(config[0]))

	def isFinished():
		"""
		sprawdzamy cz gra nie zakończyła sie 
		"""
		#for i in listaStatkow:



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
							
			shipList.append(self.__addingShip(self._config[i],(x,y),direction))						
		return shipList		







