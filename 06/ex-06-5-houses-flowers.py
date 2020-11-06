# 20K1026 日比野将己
#  課題 [5]
# --------------------------
# プログラム名: ex-06-5-houses-flowers.py

from tkinter import *


class House:
    def __init__(self, w, h, roof_color, wall_color):
        self.w = w
        self.h = h
        self.roof_color = roof_color
        self.wall_color = wall_color

    def draw(self, x, y):
        # キャンバスに自分自身を描画する。(x,y)を家の左上の座標とする。
        rtop_x = x + self.w / 2  # roof top x
        wtop_y = y + self.h / 2  # wall top y
        bottom_x = x + self.w
        bottom_y = y + self.h
        canvas.create_polygon(  # 多角形の頂点
            rtop_x, y,
            x, wtop_y,
            x + self.w, wtop_y,
            outline=self.roof_color, fill=self.roof_color)
        canvas.create_rectangle(
            x, wtop_y, bottom_x, bottom_y,
            outline=self.wall_color, fill=self.wall_color)

    def width(self):  # 図形の幅を返す
        return self.w


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

    def width(self):  # 図形の幅を返す
        return 200


tk = Tk()
canvas = Canvas(tk, width=800, height=400, bd=0, bg="whitesmoke")
canvas.pack()

objects = [
    House(50, 100, "green", "white"),
    House(100, 70, "blue", "gray"),
    Flower(100, "blue", "purple"),
    Flower(100, "red", "purple")
]

x = 0
PAD = 70
for obj in objects:
    obj.draw(x, 100)
    x = x + obj.width() + PAD

tk.mainloop()
