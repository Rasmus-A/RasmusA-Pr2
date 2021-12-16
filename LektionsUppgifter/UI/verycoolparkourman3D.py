from tkinter import *
wHeight = 800
wWidth = 260
root = Tk()
canv = Canvas(root, height=wHeight, width=wWidth, bg="green")
canv.pack()
road = canv.create_rectangle(wWidth/2 - wWidth/3, 0, wWidth/2 + wWidth/3, wHeight, fill ="grey", outline = "grey")
sky = canv.create_rectangle(0, 0, wWidth, 300, fill = "#87ceeb", outline = "#87ceeb")
player = canv.create_oval(wWidth/2 - 20, wHeight - 20, wWidth/2 + 20, wHeight - 60, fill="red")
lines = []
def lines():
    for i in range(5):
        line_y = i * 100 + 325
        line_x = 36
        for i in range(2):
            line_x += 62
            canv.create_rectangle(line_x, line_y, line_x + 3, line_y + 50, fill = "white", outline = "white")
    root.after(500)
    for i in range(5):
        line_y = i * 100 + 325
        line_x = 36
        for i in range(2):
            line_x += 62
            canv.create_rectangle(line_x, line_y, line_x + 3, line_y + 50, fill = "grey", outline = "grey")
    root.after(500)
    lines()
def move_left(e):
    if canv.coords(player)[0] >= wWidth/2 - 60:
        canv.move(player, -60, 0)
def move_right(e):
    if canv.coords(player)[0] < wWidth/2 + 30:
        canv.move(player, 60, 0)

canv.bind_all("<Left>", move_left)
canv.bind_all("<Right>", move_right)


targetDelay = 1
def animate():
    root.after(targetDelay)
root.mainloop()
lines()
