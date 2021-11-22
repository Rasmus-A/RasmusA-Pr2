try:
    import os, sys
    f = open(os.path.join(sys.path[0], "input3.in"), "r")
    input = f.read().rstrip('\n').split(" ")

    ans = 0

    N = int(input[0])
    M = int(input[1])

    diff = M - N
    if M == 0:
        ans += 20 + 10*(N%2)
    elif (diff <= 0):
        ans += 30

    elif (diff > 0):
        ans += 30
        M -= N
        ans += M//N * 10
        if M % N != 0:
            ans += 10

    print(ans)
except:
    print("Se till att du givir korrekt input!")
