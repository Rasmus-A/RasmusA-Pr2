try:
    numList = []

    amount = int(input("n: "))

    for i in range(amount):
        numList.insert(0 ,int(input(": ")))

    for i in range(amount):
        print(numList[i])
except:
    print("Endast heltal!")
