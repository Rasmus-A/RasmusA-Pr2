antalDeltagare = int(input("Antal delatagare: "))
i = 0
försvannSenast = 0
försvannInnanSenast = 1
while antalDeltagare > 0:
    antalDeltagareMem = antalDeltagare
    antalDeltagare = antalDeltagare - (försvannSenast + försvannInnanSenast)
    försvannInnanSenast = försvannSenast
    försvannSenast = antalDeltagareMem - antalDeltagare
    i += 1

print(f"Svar: {i}")
print(1)