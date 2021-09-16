x = 0

def add(*y):
    z = 0
    final = 0
    intlist = list(y)
    intlist.pop(0)  #separera till olika index först
    for i in range(y[0]):
       final = final + intlist[i]
    print(final)


str = input("ints: ")
len = len(str)
x = int(str)
add(len, x)