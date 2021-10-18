R = [[1, 1, 1, 1],
     [1, 0, 0, 1], 
     [1, 1, 1, 1], 
     [1, 1, 1, 1]]

G = [[1, 1, 1, 1],
     [1, 1, 1, 1], 
     [1, 1, 1, 1], 
     [1, 1, 1, 1]]

B = [[1, 1, 1, 1],
     [0, 1, 1, 0], 
     [0, 1, 1, 0], 
     [1, 1, 1, 1]]

checkp1 = [[0, 0, 0, 0],
           [0, 0, 0, 0], 
           [0, 0, 0, 0], 
           [0, 0, 0, 0]]

result = [[0, 0, 0, 0],
          [0, 0, 0, 0], 
          [0, 0, 0, 0], 
          [0, 0, 0, 0]]

# iterate through rows
for i in range(len(R)):
   # iterate through columns
   for j in range(len(R[0])):
       checkp1[i][j] = R[i][j] + G[i][j]

for i in range(len(checkp1)):
   # iterate through columns
   for j in range(len(checkp1[0])):
       result[i][j] = checkp1[i][j] + B[i][j]

for r in result:
   print(r)