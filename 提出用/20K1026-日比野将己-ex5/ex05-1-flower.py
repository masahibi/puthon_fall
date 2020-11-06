# 20K1026 日比野将己
# 第5回-課題[1]
# ----------------------------
# プログラム名: ex05-1-flower.py

# 花の位置と色が変えられる

from tkinter import *

x = 200
y = 100


class Flower:
    def __init__(self, size, fill1, fill2):
        self.size = size
        self.fill1 = fill1
        self.fill2 = fill2

    def draw(self, x, y):
        global canvas
        fill = self.fill1
        size = self.size
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
                x += 70
                y += 35
                size *= 0.7
                fill = self.fill2
            canvas.create_oval(x, y, x + size, y + size, fill=fill)


tk = Tk()
canvas = Canvas(tk, width=800, height=500)
canvas.pack()
flower = Flower(100, "red", "purple")
for i in range(3):
    flower.draw(x, y)
    x += 200

tk.mainloop()
