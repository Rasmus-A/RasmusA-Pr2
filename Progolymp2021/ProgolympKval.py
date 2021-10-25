top = []
right = []
left = []
bottom = []
temp = set()
score = 0
print("Give input as r, g, or b separated by a space. Going top down or left to right ")
top = input("Top row: ").split()
right = input("Right row: ").split()
left = input("Left row: ").split()
bottom = input("Bottom row: ").split()
for i in range(len(top)):
     for j in range(len(right)):
          temp.add(top[i])
          temp.add(bottom[i])
          temp.add(right[j])
          temp.add(left[j])
          if len(temp) == 3:
               score += 1
print(score)