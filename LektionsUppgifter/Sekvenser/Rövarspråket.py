text = str(input("Din text: "))
konsonanter = ["b","c","d","f","g","h","j","k","l","m","n","q","r","s","t","v","z","x"] #Kan inte hantera stora bokstäver
dic = {"b":"ob", }

j = 0
for i in text: 
    konsonantLoc = konsonanter.index(text[i])
    print(konsonantLoc)
    print(type(konsonantLoc))
    j += j
