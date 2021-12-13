from tkinter import *
wHeight = 800
wWidth = 260
root = Tk()
canv = Canvas(root, height=wHeight, width=wWidth, bg="green")
canv.pack()
road = canv.create_polygon(wWidth/2 - wWidth/5, 0, wWidth/2 + wWidth/5, 0, wWidth/2 + wWidth/3, wHeight, wWidth/2 - wWidth/3, wHeight, fill ="grey", outline = "grey")
sky = canv.create_rectangle(0, 0, wWidth, 300, fill = "#87ceeb", outline = "#87ceeb")
player = canv.create_oval(wWidth/2 - 25, wHeight - 25, wWidth/2 + 25, wHeight - 75, fill="red")
def move_left(e):
    if canv.coords(player)[0] >= wWidth/2 - 60:
        canv.move(player, -60, 0)
def move_right(e):
    if canv.coords(player)[0] < wWidth/2 + 60:
        canv.move(player, 60, 0)

canv.bind_all("<Left>", move_left)
canv.bind_all("<Right>", move_right)


targetDelay = 1
def animate():
    root.after(targetDelay)

root.mainloop()
