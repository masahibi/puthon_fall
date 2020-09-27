# 20K1026 日比野将己
# 練習課題　1.1 (1)
# ----------------------------
# プログラム名: ex01-flower-1.py

from tkinter import *

def flower(x, y, fill1, fill2):
    global canvas
    count = 0
    fill = fill1
    for i in range(5):
        if i == 0:
            x1 = x
            y1 = y
            x2 = x1
            y2 = y1 + 300
        elif i == 1:
            x1 += 100
            y1 += 50
            x2 -= 100
            y2 -= 50
        elif i == 2:
            x1 += 50
            y1 += 100
            x2 -= 50
            y2 -= 100
        elif i == 3:
            x1 -= 50
            y1 += 100
            x2 += 50
            y2 -= 100
        else:
            x1 -= 135
            y1 -= 135
            fill = fill2
            count = 1

        if count ==0:
            canvas.create_line(x1, y1, x2, y2, width=30, fill=fill)
        else:
            canvas.create_oval(x1, y1, x1 + 70, y1 + 70, fill=fill)





tk = Tk()
canvas = Canvas(tk, width=500, height=500)
canvas.pack()
flower(200, 100, "red", "purple")

canvas.mainloop()
