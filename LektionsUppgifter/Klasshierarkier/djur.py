class Djur:
    def __init__(self,namn):
        self.namn = namn

class Fagel(Djur):
    def __init__(self, namn, vingspann):
        super().__init__(namn)
        self.vingspann = vingspann

class Fisk(Djur):
    def __init__(self, namn, maxdjup):
        super().__init__(namn)
        self.maxdjup = maxdjup

class Torsk(Fisk):
    def __init__(self, namn, maxdjup, hastighet):
        super().__init__(namn, maxdjup)
        self.hastighet = hastighet

class Haj(Fisk):
    def __init__(self, namn, maxdjup, antalTänder):
        super().__init__(namn, maxdjup)
        self.antalTänder = antalTänder

def fånga(haj, torsk):
    if haj.maxdjup >= torsk.maxdjup and torsk.hastighet < 30:
        output = True
    else:
        output = False
    return output

a = Haj("Felix", 1000, 52)
b = Torsk("Torsten", 500, 30)

haj = a
torsk = b
print(fånga(haj,torsk))
