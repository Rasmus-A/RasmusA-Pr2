try:  
    import os, sys
    f = open(os.path.join(sys.path[0], "input1.in"), "r")
    input = f.read().rstrip('\n').split(" ")

    c4Area = (229 * 324)
    a3Area = (297 * 420)
    a4Area = (210 * 297)

    ans = 0
    ans += 2*(c4Area * float(input[0]))
    ans += 2*(a3Area * float(input[1]))
    ans += a4Area * float(input[2])
    ans = ans/1000000

    print("Kuvert ? " + input[0])
    print("Affisch ? " + input[1])
    print("Blad ? " + input[2])

    print("Svar:", ans)
except:
    print("Se till att du har givit korrekt input!")