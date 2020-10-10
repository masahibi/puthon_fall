# Python によるプログラミング：第 3 章
#    練習問題 3.1
# ボールは上部、左、右の3方向の壁で跳ね返る
# ボールが画面の下部に出てしまった場合ゲームオーバ
# --------------------------
# プログラム名: ex03-2-paddle.py

from tkinter import *
from dataclasses import dataclass
import random
import time

# 初期状態の設定
SPEEDS = [-3, -2, -1, 1, 2, 3]  # ボールのx方向初速選択肢
BLOCKS_X = [150, 200, 250, 300]
BLOCKS_Y = [200, 200, 300, 200]
BLOCKS_W = [40, 40, 40, 40]
BLOCKS_H = [10, 10, 10, 10]
DURATION = 0.01  # 描画間隔(秒)
BALL_X0 = 400  # ボールの初期位置(x)
BALL_Y0 = 100  # ボールの初期位置(y)
PADDLE_X0 = 350  # パドルの初期位置(x)
PADDLE_Y0 = 500  # パドルの初期位置(y)
PADDLE_VX = 5  # パドルの速度
WALL_X0 = 100
WALL_Y0 = 50
WALL_W = 400
WALL_H = 500

BALL_VX = random.choice(SPEEDS)  # ボールのx方向初速
BALL_VY = 0  # ボールのy方向初速

GRAVITY = 0.05
REACTION = 1

count1 = 0
count2 = 0

# 変える色を用意する。
COLORS = ["blue", "red", "green", "yellow", "brown", "gray"]


# -------------------------
@dataclass
class Ball:
    id: int
    x: int
    y: int
    vx: int
    vy: int
    d: int
    c: str


@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    vx: int
    c: str


@dataclass
class Wall:
    x: int
    y: int
    w: int
    h: int


@dataclass
class Block:
    x: int
    y: int
    w: int
    h: int

# -------------------------

def make_wall(wall):
    global canvas
    canvas.create_rectangle(wall.x, wall.y, wall.x+wall.w, wall.y+wall.h)
    canvas.create_line(WALL_X0, PADDLE_Y0, WALL_X0 + 50, PADDLE_Y0)
    canvas.create_line(WALL_X0 + WALL_W, PADDLE_Y0, WALL_X0 + WALL_W - 50, PADDLE_Y0)

def make_block(block, c="Blue"):
    canvas.create_rectangle(block.x, block.y, block.x + block.w, block.y + block.h, fill=c, outline=c)


# ball
# ボールの描画・登録
def make_ball(x, y, vx, vy, d=3, c="black"):
    id = canvas.create_oval(x, y, x + d, y + d,
                            fill=c, outline=c)
    return Ball(id, x, y, vx, vy, d, c)


# ボールの移動
def move_ball(ball):
    ball.x += ball.vx
    ball.vy += GRAVITY
    ball.y += ball.vy


# ボールの再描画
def redraw_ball(ball):
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + ball.d, ball.y + ball.d)


# -------------------------
# paddle
# パドルの描画・登録
def make_paddle(x, y, w=100, h=20, c="blue"):
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)
    return Paddle(id, x, y, w, h, 0, c)


# パドルの移動(左右)
def move_paddle(pad):
    pad.x += pad.vx


# パドルの色を変える
def change_paddle_color(pad, c="red"):
    canvas.itemconfigure(pad.id, fill=c)
    canvas.itemconfigure(pad.id, outline=c)
    redraw_paddle(pad)


# パドルの再描画
def redraw_paddle(pad):
    canvas.coords(pad.id, pad.x, pad.y,
                  pad.x + pad.w, pad.y + pad.h)


# -------------------------
# パドル操作のイベントハンドラ
def left_paddle(event):  # 速度を左向き(マイナス)に設定
    paddle.vx = -PADDLE_VX


def right_paddle(event):  # 速度を右向き(マイナス)に設定
    paddle.vx = PADDLE_VX


def stop_paddle(event):  # 速度をゼロに設定
    paddle.vx = 0


# =================================================
tk = Tk()
tk.title("Game")

canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# -----------------
# 描画アイテムを準備する。
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, 10)
wall = Wall(WALL_X0, WALL_Y0, WALL_W, WALL_H)
blocks = []
for x in range(4):
    blocks.append(Block(BLOCKS_X[x], BLOCKS_Y[x], BLOCKS_W[x], BLOCKS_H[x]))
make_wall(wall)
for block in blocks:
    make_block(block)

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)
canvas.bind_all('<KeyPress-Right>', right_paddle)
canvas.bind_all('<KeyRelease-Left>', stop_paddle)
canvas.bind_all('<KeyRelease-Right>', stop_paddle)

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)  # パドルの移動
    move_ball(ball)  # ボールの移動
    if ball.x + ball.vx <= wall.x:  # 左側の壁で跳ね返る
        ball.vx = -ball.vx
    if ball.x + ball.d + ball.vx >= wall.x + wall.w:  # 右の壁
        ball.vx = -ball.vx
    if ball.y + ball.vy <= wall.y:  # 上の壁
        ball.vy = -ball.vy
    if ball.y + ball.d + ball.vy >= WALL_Y0 + WALL_H:  # 下に逸らした
        break
    if paddle.x <= WALL_X0 + 50:
        paddle.x = WALL_X0 + 50
    if paddle.x + paddle.w >= WALL_X0 + WALL_W - 50:
        paddle.x = WALL_X0 + WALL_W - 50 - paddle.w
    # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
    if (paddle.y <= ball.y + ball.d <= paddle.y + paddle.h \
            and paddle.x <= ball.x + ball.d / 2 <= paddle.x + paddle.w):
        change_paddle_color(paddle, random.choice(COLORS))  # 色を変える
        ball.vy = -ball.vy * REACTION  # ボールの移動方向が変わる
    if ball.x + ball.d <= WALL_X0 + 50 and ball.y + ball.d >= PADDLE_Y0 \
            or ball.x >= WALL_X0 + WALL_W - 50 and ball.y + ball.d >= PADDLE_Y0:
        ball.vy = -ball.vy

    if ball.x + ball.d >= BLOCKS_X[0] and ball.x <= BLOCKS_X[0] + BLOCKS_W[0] and count1 == 0:
        count1 = 1
    elif ball.x + ball.d >= BLOCKS_X[1] and ball.x <= BLOCKS_X[1] + BLOCKS_W[1] and count1 == 0:
        count1 = 3
    elif ball.x + ball.d >= BLOCKS_X[2] and ball.x <= BLOCKS_X[2] + BLOCKS_W[2] and count1 == 0:
        count1 = 5
    elif ball.x + ball.d >= BLOCKS_X[3] and ball.x <= BLOCKS_X[3] + BLOCKS_W[3] and count1 == 0:
        count1 = 7
    else:
        count1 = 0
    if ball.y + ball.d >= block.y and ball.y <= block.y + block.h and count1 != 0:
        ball.vy = -ball.vy
    else:
        count1 = 0

    if ball.y + ball.d >= BLOCKS_Y[0] and ball.y <= BLOCKS_Y[0] + BLOCKS_H[0] and count2 == 0:
        count2 = 2
    elif ball.y + ball.d >= BLOCKS_Y[1] and ball.y <= BLOCKS_Y[1] + BLOCKS_H[1] and count2 == 0:
        count2 = 4
    elif ball.y + ball.d >= BLOCKS_Y[2] and ball.y <= BLOCKS_Y[2] + BLOCKS_H[2] and count2 == 0:
        count2 = 6
    elif ball.y + ball.d >= BLOCKS_Y[3] and ball.y <= BLOCKS_Y[3] + BLOCKS_H[3] and count2 == 0:
        count2 = 8
    else:
        count2 = 0
    if ball.x + ball.d >= block.x and ball.x <= block.x + block.w and count2 != 0:
        ball.vx = -ball.vx
    else:
        count2 = 0
    print(count1)
    print(count2)

    redraw_paddle(paddle)  # パドルの再描画
    redraw_ball(ball)  # ボールの再描画
    tk.update()  # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleep する。

tk.mainloop()
