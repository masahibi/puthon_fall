# 20K1026 日比野将己
# 第5回-課題[2]
# --------------------------
# プログラム名: ex05-2-ball.py

from tkinter import *
from dataclasses import dataclass
import random
import time

# 初期状態の設定
SPEEDS = [-3, -2, -1, 1, 2, 3]  # ボールのx方向初速選択肢
DURATION = 0.01  # 描画間隔(秒)
BALL_X0 = 400  # ボールの初期位置(x)
BALL_Y0 = 100  # ボールの初期位置(y)
PADDLE_X0 = 350  # パドルの初期位置(x)
PADDLE_Y0 = 500  # パドルの初期位置(y)
PADDLE_VX = 5  # パドルの速度

BALL_VX = random.choice(SPEEDS)  # ボールのx方向初速
BALL_VY = 0  # ボールのy方向初速

WALL_X = 100
WALL_Y = 100
WALL_W = 600
WALL_H = 400
GRAVITY = 0.1
REACTION = 1.01

# 変える色を用意する。
COLORS = ["blue", "red", "green", "yellow", "brown", "gray"]


# -------------------------

class Ball:
    def __init__(self, id, x, y, vx, vy, d, c):
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.d = d
        self.c = c

    # ボールの移動
    def move_ball(self):  # ボールの移動関数
        self.x += self.vx  # x を vx 分移動させる
        self.vy += GRAVITY  # vy　に重力加える
        self.y += self.vy  # y を vy 分移動させる

    # ボールの再描画
    def redraw_ball(self):  # ボールの再描写関数
        global canvas
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)  # id の値を変更する


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


# -------------------------

def make_wall(wall):  # 外枠の作成関数
    global canvas
    canvas.create_rectangle(wall.x, wall.y, wall.x + wall.w, wall.y + wall.h, width=3)  # 外枠作成


# ball
# ボールの描画・登録
def make_ball(x, y, vx, vy, d=3, c="black"):  # ボールの作成関数
    id = canvas.create_oval(x, y, x + d, y + d,
                            fill=c, outline=c)  # id にボールの初期値を代入
    return Ball(id, x, y, vx, vy, d, c)  # id を加えて返す


# -------------------------
# paddle
# パドルの描画・登録
def make_paddle(x, y, w=100, h=20, c="blue"):  # パドルの作成関数
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)  # id にパドルの初期値を保存
    return Paddle(id, x, y, w, h, 0, c)  # id を加えて返す


# パドルの移動(左右)
def move_paddle(pad):  # パドルの移動関数
    pad.x += pad.vx  # x を vx 分移動させる


# パドルの色を変える
def change_paddle_color(pad, c="red"):  # パドルの色を変える関数
    canvas.itemconfigure(pad.id, fill=c)  # fill を c にする
    canvas.itemconfigure(pad.id, outline=c)  # outline を c にする
    redraw_paddle(pad)  # パドルの再描写


# パドルの再描画
def redraw_paddle(pad):  # パドルの再描写関数
    canvas.coords(pad.id, pad.x, pad.y,
                  pad.x + pad.w, pad.y + pad.h)  # id の値を変更する


# -------------------------
# パドル操作のイベントハンドラ
def left_paddle(event):  # 速度を左向き(マイナス)に設定
    paddle.vx = -PADDLE_VX  # パドルを左に動かす


def right_paddle(event):  # 速度を右向き(マイナス)に設定
    paddle.vx = PADDLE_VX  # パドルを右に動かす


def stop_paddle(event):  # 速度をゼロに設定
    paddle.vx = 0  # パドルを止める


# =================================================
tk = Tk()
tk.title("Game")

canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# -----------------
# 描画アイテムを準備する。
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)  # 実際にパドルを描写する
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, 10)  # 実際にボールを描写する
wall = Wall(WALL_X, WALL_Y, WALL_W, 400)  # 外枠の作成
make_wall(wall)  # 実際に外枠を描写する

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)  # 左押したら、パドルが左に移動する
canvas.bind_all('<KeyPress-Right>', right_paddle)  # 右押したら、パドルが右に移動する
canvas.bind_all('<KeyRelease-Left>', stop_paddle)  # 左離したら、パドルが止まる
canvas.bind_all('<KeyRelease-Right>', stop_paddle)  # 右離したら、パドルが止まる

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)  # パドルの移動
    Ball.move_ball(ball)  # ボールの移動
    if ball.x + ball.vx <= wall.x:  # 左側の壁を越えたら
        ball.vx = -ball.vx  # 反射させる
    if ball.x + ball.d + ball.vx >= wall.x + wall.w:  # 右の壁を越えたら
        ball.vx = -ball.vx  # 反射させる
    if ball.y + ball.vy <= wall.y:  # 上の壁を越えたら
        ball.vy = -ball.vy  # 反射させる
    if ball.y + ball.d + ball.vy >= 600:  # キャンバスの下についたら
        break  # ループを抜ける
    if paddle.x <= 0:  # パドルがキャンバスの左についたら
        paddle.x = 0  # パドルを止める
    if paddle.x + paddle.w >= 800:  # パドルがキャンバスの右についたら
        paddle.x = 800 - paddle.w  # パドルを止める
    # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
    if (paddle.y <= ball.y + ball.d <= paddle.y + paddle.h \
            and paddle.x <= ball.x + ball.d / 2 <= paddle.x + paddle.w):  # パドルにボールが当たったら
        change_paddle_color(paddle, random.choice(COLORS))  # 色を変える
        ball.vy = -ball.vy * REACTION  # ボールの移動方向が変わる

    redraw_paddle(paddle)  # パドルの再描画
    Ball.redraw_ball(ball)  # ボールの再描画
    tk.update()  # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleep する。

tk.mainloop()
