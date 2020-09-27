# Pythonによるプログラミング：第1章
#    練習問題 1-3
# --------------------------
# プログラム名: ex01-ellipses.py

from tkinter import *
import math

OX = 400    # (OX, OY)がキャンバス上での原点の位置
OY = 300
MAX_X = 800  # 座標軸の最大(キャンバス座標)
MAX_Y = 600
SCALE_X = 100 # キャンバス座標への変換係数
SCALE_Y = 100

START = 0
END = 2*math.pi
DELTA = 0.01

def draw_point(x, y, r=2, c="black"):    # 変更点
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline=c)

def make_axes(ox, oy, width, height):
    canvas.create_line(0, oy, width, oy)
    canvas.create_line(ox, 0, ox, height)

def plot(x, y, r=1, c="black"):
    draw_point(SCALE_X * x + OX, OY - SCALE_Y * y, r, c)

def f1(x):
    return math.cos(x)

def f2(x):
    return math.sin(x)

tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()

make_axes(OX, OY, MAX_X, MAX_Y)

theta = START
while theta < END:
    plot(f1(theta), f2(theta))
    plot(f1(theta)/2, 2 * f2(theta), 1, "blue")
    theta = theta + DELTA

canvas.mainloop()