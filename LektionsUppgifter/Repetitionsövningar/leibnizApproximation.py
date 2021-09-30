j = 3
x = 1
for i in range(15):
    x -= 1/j
    j += 2
    x += 1/j
    j += 2

x = x*4
print(x)
