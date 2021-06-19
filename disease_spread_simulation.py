import random
import matplotlib.pyplot as plt

#parametry wejsciowe
wymiar_planszy = 100 #10 000 pol
wielkosc_populacji = 500
ilosc_tur = 50

class Osobnik:
    def __init__(self):
        self.zywy = 1
        self.polozenie = [random.randint(0, wymiar_planszy - 1), random.randint(0, wymiar_planszy - 1)]
        self.predkosc = random.randint(1, wymiar_planszy/10)
        self.kierunek = random.choice(['prawo', 'lewo', 'gora', 'dol'])
        self.stan = random.choice(['Z', 'C', 'ZD', 'ZZ'])
        self.liczba_tur_od_zmiany_stanu = 0
        self.wiek = 0
        self.odpornosc = 2.0
        self.max_odpornosc = 3.0

    def dodajTure(self):
        if (self.zywy == 1): self.obliczStanIOdpornoscNaPoczatkuTury()
        if (self.zywy == 1): self.obliczRuch()

    def obliczStanIOdpornoscNaPoczatkuTury(self):
        self.wiek += 1
        self.liczba_tur_od_zmiany_stanu += 1

        if (self.wiek == 15):
            self.max_odpornosc = 10.0
        if (self.wiek == 40):
            self.max_odpornosc = 6.0
        if (self.wiek == 70):
            self.max_odpornosc = 3.0

        if (self.stan == 'Z'):
            self.odpornosc -= 0.1
            if (self.liczba_tur_od_zmiany_stanu == 2):
                self.stan = 'C'
        if (self.stan == 'C'):
            self.odpornosc -= 0.5
            if (self.liczba_tur_od_zmiany_stanu == 7):
                self.stan = 'ZD'
        if (self.stan == 'ZD'):
            self.odpornosc += 0.1
            if (self.liczba_tur_od_zmiany_stanu == 5):
                self.stan = 'ZZ'
        if (self.stan == 'ZZ'):
            self.odpornosc += 0.5

        if (self.odpornosc > self.max_odpornosc):
            self.odpornosc = self.max_odpornosc

        if (self.odpornosc <= 0): self.zywy = 0
        
    def obliczRuch(self):
        if (self.kierunek == 'prawo'): self.polozenie[0] += self.predkosc
        if (self.kierunek == 'lewo'): self.polozenie[0] -= self.predkosc
        if (self.kierunek == 'gora'): self.polozenie[1] += self.predkosc
        if (self.kierunek == 'dol'): self.polozenie[1] -= self.predkosc

        if (self.polozenie[0] >= (wymiar_planszy - 1)):
            self.kierunek = 'lewo'
            self.polozenie[0] =  wymiar_planszy - 1 - (self.polozenie[0] - wymiar_planszy +1) # +1 i -1 wynikaja z indeksowania listy od 0
        if (self.polozenie[1] >= (wymiar_planszy - 1)):
            self.kierunek = 'dol'
            self.polozenie[1] = wymiar_planszy - 1 - (self.polozenie[1] - wymiar_planszy +1)
        if (self.polozenie[0] <= 0):
            self.kierunek = 'prawo'
            self.polozenie[0] = 0 - self.polozenie[0]
        if (self.polozenie[1] <= 0):
            self.kierunek = 'prawo'
            self.polozenie[1] = 0 - self.polozenie[1]

    def kontakt(self, sasiad):
        stan_sasiada = sasiad.stan

        if (self.stan == 'ZZ'):
            if (stan_sasiada == 'ZZ'):
                if (self.odpornosc <= 3): self.stan = 'Z'
            if (stan_sasiada == 'C'):
                if (self.odpornosc > 6): self.odpornosc -= 3
                else: self.stan = 'Z'
            if (stan_sasiada == 'ZZ' and sasiad.odpornosc > self.odpornosc):
                if (sasiad.odpornosc < self.max_odpornosc): self.odpornosc = sasiad.odpornosc
                else: self.odpornosc = self.max_odpornosc
        if (self.stan == 'C'):
            if (stan_sasiada == 'Z'): self.liczba_tur_od_zmiany_stanu = 0
            if (stan_sasiada == 'C' and sasiad.odpornosc < self.odpornosc): self.odpornosc = sasiad.odpornosc
        if (self.stan == 'Z'):
            if (stan_sasiada == 'C'):
                if (self.odpornosc <= 6): self.stan = 'C'
        if (self.stan == 'ZD'):
            if (stan_sasiada == 'ZZ'): self.odpornosc += 1
            if (stan_sasiada == 'C' and self.odpornosc <= 3): self.stan = 'Z'
            if (stan_sasiada == 'Z'): self.odpornosc -= 1
            

def rysujPunkty(osobniki):
    osobniki_polozenie_Z = [o.polozenie for o in osobniki if o.stan == 'Z' and o.zywy == 1]
    osobniki_polozenie_C = [o.polozenie for o in osobniki if o.stan == 'C' and o.zywy == 1]
    osobniki_polozenie_ZD = [o.polozenie for o in osobniki if o.stan == 'ZD' and o.zywy == 1]
    osobniki_polozenie_ZZ = [o.polozenie for o in osobniki if o.stan == 'ZZ' and o.zywy == 1]
    if (osobniki_polozenie_Z): plt.scatter(*zip(*osobniki_polozenie_Z), color = 'yellow')
    if (osobniki_polozenie_C): plt.scatter(*zip(*osobniki_polozenie_C), color = 'red')
    if (osobniki_polozenie_ZD): plt.scatter(*zip(*osobniki_polozenie_ZD), color = 'orange')
    if (osobniki_polozenie_ZZ): plt.scatter(*zip(*osobniki_polozenie_ZZ), color = 'green')
    plt.pause(0.5)
    plt.clf()

def dodajTure():
    global licznik_tur
    global osobniki

    licznik_tur += 1
    for osobnik in osobniki:
        osobnik.dodajTure()

    rysujPunkty(osobniki)

    #dodanie osobnikow do tablicy by zidentyfikowac kontakty
    tablica_osobnikow = [ [None] * wymiar_planszy for i in range(wymiar_planszy)]

    for osobnik in osobniki:
        if (osobnik.zywy == 1): tablica_osobnikow[osobnik.polozenie[0]][osobnik.polozenie[1]] = osobnik

    for o in osobniki:
        x1 = o.polozenie[0]
        y1 = o.polozenie[1]
        sasiedzi = []

        for x in [x1 - 1, x1, x1 + 1]:
            for y in [y1 - 1, y1, y1 +1]:
                if (x >= 0 and x < wymiar_planszy and y >= 0 and y < wymiar_planszy):
                    if (tablica_osobnikow[x][y] != None): sasiedzi.append(tablica_osobnikow[x][y])

        for sasiad in sasiedzi:
            o.kontakt(sasiad)

    # print(tablica_osobnikow)

licznik_tur = 0
osobniki = [Osobnik() for i in range(wielkosc_populacji)]
print('symulacja zainicjalizowana')
print(len(osobniki))

plt.ion()

for i in range(ilosc_tur):
    dodajTure()

plt.ioff()
plt.show()

# for o in osobniki:
#     print(o.stan)
