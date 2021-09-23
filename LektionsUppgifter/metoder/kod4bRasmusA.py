import numpy as np
x = -0.5
numpy_log_val = np.log(1+x)
checksum = 1/10000000
log_serie_10 = x
temp = 0
i = 0
while abs(numpy_log_val - log_serie_10) > (checksum):
    temp = ((x)**(i+2))/(i+2)

    if (i+2) % 2 == 0:
        log_serie_10 -= temp

    elif (i+2) % 2 != 0:
        log_serie_10 += temp
    
    i += 1
    print(i)

print(numpy_log_val - log_serie_10)
print(log_serie_10)
print(numpy_log_val)