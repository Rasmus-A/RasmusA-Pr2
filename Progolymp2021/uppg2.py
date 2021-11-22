try:
    import os, sys
    f = open(os.path.join(sys.path[0], "input2.in"), "r")
    input = f.read().rstrip('\n').split(" ")

    vowels = ["a", "e", "i", "o", "u", "y"]

    sentence = ""
    for i in range(int(input[0])):
        sentence += " "
        sentence += input[i+1]

    for j in range(len(sentence)):
        if (len(sentence) - j > 2):
            if any(check in sentence[j] for check in vowels) == True:
                if (any(check in sentence[j+1] for check in vowels) == False) and (any(check in sentence[j+2] for check in vowels) == False) and (sentence[j+1] != " ") and (sentence[j+2] != " "):
                    sentence = sentence[:j] + sentence[j+1:]

    revSentence = sentence[::-1]

    print("Antal ord ?", input[0])
    print(revSentence)
except:
    print("Se till att du givit korrekt input!")