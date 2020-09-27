# 20K1026 日比野将己
# 練習問題 1-3
# --------------------------
# プログラム名: ex01-ellipses.py

from tkinter import *
import math

OX = 400  # (OX, OY)がキャンバス上での原点の位置
OY = 300
MAX_X = 800  # 座標軸の最大(キャンバス座標)
MAX_Y = 600
SCALE_X = 100  # キャンバス座標への変換係数
SCALE_Y = 100

START = 0  # 0から
END = 2 * math.pi    # 2πまで
DELTA = 0.01    # プロット間隔


def draw_point(x, y, r=1, c="black"):  # 点1つ
    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline=c)    # 円書くやつ


def make_axes(ox, oy, width, height):    # 軸作成
    canvas.create_line(0, oy, width, oy)    # x軸
    canvas.create_line(ox, 0, ox, height)    # y軸


def plot(x, y, r=1, c="black"):    # プロットしていく場所
    draw_point(SCALE_X * x + OX, OY - SCALE_Y * y, r, c)    # 上の draw_point


def f1(x):    # グラフにする関数
    return math.cos(x)    # cosx


def f2(x):    # グラフにする関数
    return math.sin(x)    # sinx


tk = Tk()
canvas = Canvas(tk, width=800, height=600, bd=0)
canvas.pack()

make_axes(OX, OY, MAX_X, MAX_Y)    # グラフの軸作成

theta = START    # 0
while theta < END:    # 2π
    plot(f1(theta), f2(theta), 2)    # グラフ描写（円）
    plot(f1(theta) / 2, 2 * f2(theta), 1, "blue")    # グラフ描写（楕円）
    theta = theta + DELTA    # プロット間隔

tk.mainloop()
