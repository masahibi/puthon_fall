# 20K1026 日比野将己
# 練習問題 1-2 (1)
# --------------------------
# プログラム名: ex01-cubic.py

from tkinter import *
import math

OX = 400  # (OX, OY)がキャンバス上での原点の位置
OY = 400
MAX_X = 800  # 座標軸の最大(キャンバス座標)
MAX_Y = 800
SCALE_X = 20  # キャンバス座標への変換係数
SCALE_Y = 10

START = -5.0  # -5 から
END = 5.0  # 5 まで
DELTA = 0.001    # プロット間隔


def draw_point(x, y, r=1, c="black"):  # 点1つ
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline=c)    # 円書くやつ


def make_axes(ox, oy, width, height):    # 軸作成
    canvas.create_line(0, oy, width, oy)    # x軸
    canvas.create_line(ox, 0, ox, height)    # y軸


def plot(x, y):    # プロットする場所
    draw_point(SCALE_X * x + OX, OY - SCALE_Y * y)    # 上の draw_point


def f(x):    # グラフにする関数
    return x ** 3 + x ** 2 - 8 * x - 12  # x^3 + x^2 - 8x - 12


tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()

make_axes(OX, OY, MAX_X, MAX_Y)    # グラフの軸作成

x = START    # -5
while x < END:    # 5
    plot(x, f(x))    # グラフ描写
    x = x + DELTA    # プロット間隔
tk.mainloop()
