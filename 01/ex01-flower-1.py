# 20K1026 日比野将己
# 練習課題　1.1 (1)
# ----------------------------
# プログラム名: ex01-flower-1.py

from tkinter import *


def flower(x, y, fill1, fill2):
    global canvas
    fill = fill1
    size = 100
    for i in range(6):
        if i == 0:
            x = x
            y = y
        elif i == 1:
            x += 50
            y += 50
        elif i == 2:
            x -= 25
            y += 50
        elif i == 3:
            x -= 60
            y += 0
        elif i == 4:
            x -= 20
            y -= 60
        else:
            x += 75
            y += 35
            size *= 0.6
            fill = fill2
        canvas.create_oval(x, y, x + size, y + size, fill=fill)


tk = Tk()
canvas = Canvas(tk, width=500, height=500)
canvas.pack()
flower(213, 200, "red", "purple")

canvas.mainloop()
