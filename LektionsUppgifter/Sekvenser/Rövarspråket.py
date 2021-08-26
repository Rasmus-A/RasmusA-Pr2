text = str(input("Din text: "))
konsonanter = ["b","c","d","f","g","h","j","k","l","m","n","q","r","s","t","v","z","x"] #Kan inte hantera stora bokstäver
dic = {}

j = 0
for i in text: 
    konsonantLoc = konsonanter.index(text[j])
    print (konsonantLoc)
    type(konsonantLoc)
    j += j
