# 20K1026 日比野将己
# 練習問題 1-2 (2)
# --------------------------
# プログラム名: ex01-cos.py

from tkinter import *
import math

OX = 100  # (OX, OY)がキャンバス上での原点の位置
OY = 300
MAX_X = 800  # 座標軸の最大(キャンバス座標)
MAX_Y = 600
SCALE_X = 40  # キャンバス座標への変換係数
SCALE_Y = 40

START = 0    # cos0 から
END = 4 * math.pi    # cos4π まで
DELTA = 0.01    # プロットする間隔


def draw_point(x, y, r=1, c="black"):    # 点1つ
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline=c)    # 円書くやつ


def make_axes(ox, oy, width, height):    # 軸作成
    canvas.create_line(0, oy, width, oy)    # X軸
    canvas.create_line(ox, 0, ox, height)    # Y軸


def plot(x, y):    # 点打っていく場所
    draw_point(SCALE_X * x + OX, OY - SCALE_Y * y)    # 上の draw_point


def f(x):    # 作成する関数
    return math.cos(x)  # cosx


tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()

make_axes(OX, OY, MAX_X, MAX_Y)    # グラフの軸作成

x = START    # 0
while x < END:    # 4π
    plot(x, f(x))    # 打点
    x = x + DELTA    # プロット間隔

tk.mainloop()
