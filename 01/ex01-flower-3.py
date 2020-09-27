from tkinter import *


def flower(x, y, fill1, fill2):
    global canvas
    count = 0
    fill = fill1

    for i in range(5):
        if i == 0:
            x1 = x
            y1 = y
            x2 = x1 + 100
            y2 = y1
            x3 = x1 + 50
            y3 = y1 + 100
        elif i == 1:
            x1 += 50
            y1 += 100
            x2 += 50
            y2 += 50
            x3 = x2
            y3 += 50
        elif i == 2:
            x1 = x1
            y1 = y1
            x2 -= 50
            y2 += 150
            x3 -= 150
            y3 = y2
        elif i == 3:
            x1 -= 100
            y1 -= 50
            x2 -= 50
            y2 -= 100
            x3 = x1
            y3 -= 50
        else:
            count = 1
            x1 = x2 - 20
            y1 = y2 - 20
            fill = fill2
            canvas.create_oval(x1, y1, x1 + 40, y1 + 40, fill=fill)
        if count == 0:
            canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=fill)


tk = Tk()
canvas = Canvas(tk, width=500, height=500)
canvas.pack()
flower(200, 100, "red", "purple")

canvas.mainloop()
