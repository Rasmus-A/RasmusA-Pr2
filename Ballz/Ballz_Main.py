from tkinter import *
import math
import random as rand

root = Tk()

global blueBallPurchased, greenBallPurchased, goldBallPurchased, ballEquiped, totalScore, blueBallText
totalScore = 0
ballEquiped = "red"
blueBallPurchased = False
greenBallPurchased = False
goldBallPurchased = False
blueBallText = "Purchase, 1000 score"
greenBallText = "Purchase, 1000 score"
goldBallText = "Purchase, 2000 score"
h = 800
w = 1000
root.resizable(width = False, height = False)
canv = Canvas(root, height = h, width = w, bg = "white")
canv.pack()
id = canv.create_oval(100, 100, 150, 150, fill = ballEquiped)

def update_circle():
    global clickable
    clickable = True
    canv.itemconfig(id, fill = ballEquiped, outline = "black")
    randomX =  rand.randint(0, w - 50)
    randomY = rand.randint(0, h - 50)
    canv.coords(id, randomX, randomY, randomX + 50, randomY + 50)
    canv.update()
    root.after(1500, update_circle) 

def clickCheck(event):
    global clickable, totalScore
    distanceToCenter = math.sqrt((((canv.coords(id)[0] + 25) - event.x)**2) + (((canv.coords(id)[1] + 25) - event.y)**2))
    if clickable == True and event.x > canv.coords(id)[0] and event.x < canv.coords(id)[2] and event.y > canv.coords(id)[1] and event.y < canv.coords(id)[3] and distanceToCenter < 25:
        canv.itemconfig(id, fill = "white", outline = "white")
        clickable = False
        totalScore += 100

def shop():
    global greenB, blueB, goldB
    shopH = 75
    shopW = 356
    shopWindow = Toplevel()
    shopWindow.title("shop")
    shopCanv = Canvas(shopWindow, height=shopH, width=shopW, bg="white")
    shopCanv.pack()
    shopWindow.resizable(width=False, height=False)

    blueBall = shopCanv.create_oval(shopW/2 - 145, shopH/2 - 25, shopW/2 - 95, shopH/2 + 25, fill="blue")
    greenBall = shopCanv.create_oval(shopW/2 - 25, shopH/2 - 25, shopW/2 + 25, shopH/2 + 25, fill="green")
    goldBall = shopCanv.create_oval(shopW/2 + 95, shopH/2 - 25, shopW/2 + 145, shopH/2 + 25, fill="gold")

    labelTopFrame = Frame(shopWindow)
    labelTopFrame.pack(fill = "both")

    buttonBotFrame = Frame(shopWindow)
    buttonBotFrame.pack(side = BOTTOM, fill = "both")

    blueL = Label(labelTopFrame, text = "Blue Ball")
    greenL = Label(labelTopFrame, text = "Green Ball")
    goldL = Label(labelTopFrame, text = "Gold Ball")

    blueB = Button(buttonBotFrame, text = blueBallText, width = 16, command = purchaseBlueBall)
    greenB = Button(buttonBotFrame, text = greenBallText, width = 16, command = purchaseGreenBall)
    goldB = Button(buttonBotFrame, text = goldBallText, width = 16, command = purchaseGoldBall)

    blueL.pack(side = LEFT, padx = 35)
    greenL.pack(side = LEFT, padx = 30)
    goldL.pack(side = LEFT, padx = 35)
    blueB.pack(side = LEFT)
    greenB.pack(side = LEFT)
    goldB.pack(side = LEFT)

def purchaseBlueBall():
    global blueBallPurchased, ballEquiped, totalScore, blueB, blueBallText
    if blueBallPurchased == False and totalScore >= 1000:
        blueBallPurchased = True
        totalScore -= 1000
        blueB.config(text = "Equip")
        blueBallText = "Equip"
    elif blueBallPurchased == True and ballEquiped == "blue":
        ballEquiped = "red"
        blueB.config(text = "Equip")
        blueBallText = "Equip"
    elif blueBallPurchased == True:
        ballEquiped = "blue"
        blueB.config(text = "Unequip")
        blueBallText = "Unequip"


def purchaseGreenBall():
    global greenBallPurchased, ballEquiped, totalScore, greenBallText
    if greenBallPurchased == False and totalScore >= 1000:
        greenBallPurchased = True
        totalScore -= 1000
        greenB.config(text = "Equip")
        greenBallText = "Equip"
    elif greenBallPurchased == True and ballEquiped == "green":
        ballEquiped = "red"
        greenB.config(text = "Equip")
        greenBallText = "Equip"
    elif greenBallPurchased == True:
        ballEquiped = "green"
        greenB.config(text = "Unequip")
        greenBallText = "Uneuip"

def purchaseGoldBall():
    global goldBallPurchased, ballEquiped, totalScore, goldBallText
    if goldBallPurchased == False and totalScore >= 2000:
        goldBallPurchased = True
        totalScore -= 2000
        goldB.config(text = "Equip")
        goldBallText = "Equip"
    elif goldBallPurchased == True and ballEquiped == "gold":
        ballEquiped = "red"
        goldB.config(text = "Equip")
        goldBallText = "Equip"
    elif goldBallPurchased == True:
        ballEquiped = "gold"
        goldB.config(text = "Unequip")
        goldBallText = "Unequip"

    

menuFrame = Frame()
menuFrame.pack(side = BOTTOM, fill = "both")

shopB = Button(menuFrame, text ="Shop", command = shop)
shopB.pack(side = LEFT)

scoreTextL = Label(menuFrame, text = "Score: ")
scoreTextL.pack(side = LEFT)

scoreLabelText = IntVar()
scoreL = Label(menuFrame, textvariable = scoreLabelText)
scoreL.pack(side = LEFT)
scoreLabelText.set(totalScore)
scoreL.update()

canv.bind('<Button-1>', clickCheck)
root.after(1500, update_circle) 
root.mainloop()