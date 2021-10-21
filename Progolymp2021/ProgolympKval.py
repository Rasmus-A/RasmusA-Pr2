top = []
right = []
left = []
bottom = []
temp = []
score = 0


print("Give input as r, g, or b separated by a space x4. Going top down or left to right ")
top = input("Top row: ").split()
right = input("Right row: ").split()
left = input("Left row: ").split()
bottom = input("Bottom row: ").split()

for i in range(4):
     for j in range(4):
          full = ["r", "g", "b"]
          temp.append(top[i])
          temp.append(bottom[i])
          temp.append(right[j])
          temp.append(left[j])
          pairs = ([(value, "True") for value in temp])
          for a, b in pairs:
               if a == True:
                    full.remove(b)
          print(full)
          temp.clear()

#print(score)