"""diff = 0
try: 
    antal_banor = int(input("Ange antal banor: "))
    for i in range(antal_banor):
        antal_slag = int(input("Ange slag bana "+str(i+1)+":"))
        if antal_slag > 7: 
            antal_slag = 7
        if (i+1)%2 == 0: 
            diff += -3+antal_slag
        elif (i+1)%2 == 1: 
            diff += -2+antal_slag
    print(diff)
except: print("Fel input!")
"""
all = ""
antal_sidor = int(input("Anta sidor: "))
for i in range(antal_sidor):
    if (i+1)%2 != 0:
        all += (str(i+1))
nollor = all.count("0")
ettor = all.count("1")
tvåor = all.count("2")
treor = all.count("3")
fyror = all.count("4")
femmor = all.count("5")
sexor = all.count("6")
sjuor = all.count("7")
åttor = all.count("8")
nior = all.count("9")
print(nollor, ettor, tvåor, treor, fyror, femmor, sexor, sjuor, åttor, nior)