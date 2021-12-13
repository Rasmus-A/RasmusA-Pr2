
class Djur:
    def __init__(self,namn):
        self.namn = namn

    def at(self):
        print('Djuret åt')
    def sov(self):
        print('Djuret sover')

class Fagel(Djur):
    def __init__(self, namn, vingspann):
        super().__init__(namn)
        self.vingspann = vingspann

class Fisk(Djur):
    def __init__(self, namn, maxdjup):
        super().__init__(namn)
        self.maxdjup = maxdjup

    def simma(self):
        print('fisken simmar')

class Torsk(Fisk):
    def __init__(self, namn, maxdjup, hastighet):
        super().__init__(namn, maxdjup)
        self.hastighet = hastighet

class Haj(Fisk):
    def __init__(self, namn, maxdjup, antalTänder):
        super().__init__(namn, maxdjup)
        self.antalTänder = antalTänder

    def at(self, djur):
        print(self.namn, 'åt', djur.namn)

def fånga(haj, torsk):
    if haj.maxdjup >= torsk.maxdjup and torsk.hastighet < 30:
        output = True
    else:
        output = False
    return output

a = Haj("Felix", 1000, 52)
b = Torsk("Torsten", 500, 30)

b.simma()

a.at(b)

haj = a
torsk = b
print(fånga(haj,torsk))


class Fordon:
    def kör(self):
        print("Nu kör vi!")
class Bil(Fordon):
    def tuta(self):
        print("Tuuut!!")
class Sportbil(Bil):
    def kör(self):
        print("Nu kör sportbilen!")
class Cykel(Fordon):
    def plinga(self):
        print("Pling!")

c = Cykel()
b = Sportbil()
b.kör()     # anropar en Fordon-metod i ett Bil-objekt
b.tuta()    # anropar en Bil-metod
c.plinga()
