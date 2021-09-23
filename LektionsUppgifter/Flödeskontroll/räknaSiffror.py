string = input("sträng: ")
numCount = 0
num = ["0","1","2","3","4","5","6","7","8","9"]
for i in string:
    if i in num: 
        numCount += 1
print(numCount)