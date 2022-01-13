from tkinter import *
import math
root = Tk()
h = 800
w = 1000
global ballEquiped
ballEquiped = "red"
root.resizable(width=False, height=False)
canv = Canvas(root, height=h, width=w, bg="white")
canv.pack()
id = canv.create_oval(0, 100, 50, 150, fill=ballEquiped)

blueBallPurchased = False
greenBallPurchased = False
goldBallPurchased = False


def distance(x1, x2, y1, y2):
    calculatedDistance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return calculatedDistance

def angle(x1, x2, y1, y2):
    calculatedAngle = math.atan2(y2-y1, x2-x1)
    return calculatedAngle

def startAim(event):
    global startPoint
    startPoint = (event.x, event.y)
    print(startPoint)
def endAim(event):
    global startPoint 
    endPoint = (event.x, event.y)
    print(endPoint)
    shotPower = distance(startPoint[0], endPoint[0], startPoint[1], endPoint[1])
    print(shotPower)
    shotAngle = angle(startPoint[0], endPoint[0], startPoint[1], endPoint[1])
    print(shotAngle)
    startPoint = (0, 0)

def currentMouseLocation(event):
    global currentMouseX
    global currentMouseY
    currentMouseX = event.x
    currentMouseY = event.y

#def aimVisualizer():
#   
#   if startPoint[0] > 0:
#        aimLine = canv.create_line(startPoint[0], startPoint[1], currentMouseX, currentMouseY)
#        canv.delete(aimLine)
#        aimLine = canv.create_line(startPoint[0], startPoint[1], currentMouseX, currentMouseY)
#        root.after(1, aimVisualizer)

def purchaseBlueBall():
    blueBallPurchased = True
    ballEquiped = "blue"
    canv.update()

def purchaseGreenBall():
    greenBallPurchased = True
    ballEquiped = "green"
    canv.update()

def purchaseGoldBall():
    if goldBallPurchased = False:
        goldBallPurchased = True
        ballEquiped = "gold"
        canv.update()
    else ballEquiped = "gold"


def shop():
    shopH = 75
    shopW = 356
    shopWindow = Toplevel()
    shopWindow.title("shop")
    shopCanv = Canvas(shopWindow, height=shopH, width=shopW, bg="white")
    shopCanv.pack()
    shopWindow.resizable(width=False, height=False)

    blueBall = shopCanv.create_oval(shopW/2 - 25, shopH/2 - 25, shopW/2 + 25, shopH/2 + 25, fill="blue")
    greenBall = shopCanv.create_oval(shopW/2 - 25, shopH/2 - 25, shopW/2 + 25, shopH/2 + 25, fill="green")
    goldBall = shopCanv.create_oval(shopW/2 - 25, shopH/2 - 25, shopW/2 + 25, shopH/2 + 25, fill="gold")
    if blueBallPurchased == True:
        blueBallText = "Equip"
    else:
        blueBallText = "Purchase, 1000 score"
    if greenBallPurchased == True:
        greenBallText = "Equip"
    else:
        greenBallText = "Purchase, 1000 score"
    if goldBallPurchased == True:
        goldBallText = "Equip"
    else:
        goldBallText = "Purchase, 1000 score"
        
    blueB = Button(shopWindow, text = blueBallText, width = 16, command = purchaseBlueBall)
    greenB = Button(shopWindow, text = greenBallText, width = 16, command = purchaseGreenBall)
    goldB = Button(shopWindow, text = goldBallText, width = 16, command = purchaseGoldBall)

    blueB.pack(side = LEFT)
    greenB.pack(side = LEFT)
    goldB.pack(side = LEFT)
    


shopB = Button(root, text ="Shop", command = shop)
shopB.pack()


canv.bind('<Button-1>', startAim)
canv.bind('<ButtonRelease-1>', endAim)
canv.bind('<Motion>', currentMouseLocation)
#root.after(1000, aimVisualizer)


root.mainloop()
