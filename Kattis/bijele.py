input = input("Sträng: ")
inputList = input.split(" ")
output = ""
try:
    for i in range(6):
        if i == 0 or i == 1:
            output += str(1-int(inputList[i]))
        if i == 2 or i == 3 or i == 4:
            output += str(2-int(inputList[i]))
        if i == 5:
            output += str(8-int(inputList[i]))
        output += " "
    print(output)
except:
    print("nej")