# 20K1026 日比野将己
# 練習問題 3-1-1
# --------------------------
# プログラム名: ex03-paddle.py

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
BALL_VY = 3  # ボールのy方向初速

WALL_X = 100    # 外枠のx座標
WALL_Y = 100    # 外枠のｙ座標
WALL_W = 600    # 外枠の幅
WALL_H = 400    # 外枠の高さ


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


# -------------------------

def make_wall(wall):    # 外枠を作る関数
    global canvas
    canvas.create_rectangle(wall.x, wall.y, wall.x+wall.w, wall.y+wall.h, width=3)    # 外枠作成（太くしたらレトロっぽくなったｗ）


# ball
# ボールの描画・登録
def make_ball(x, y, vx, vy, d=3, c="black"):    # ボールを作成する関数
    global canvas
    id = canvas.create_oval(x, y, x + d, y + d,
                            fill=c, outline=c)    # id にボールの初期情報を保存
    return Ball(id, x, y, vx, vy, d, c)    # id を加えて返す


# ボールの移動
def move_ball(ball):    # ボールの移動先の関数
    ball.x += ball.vx    # x を vx 分移動させる
    ball.y += ball.vy    # y を vy 分移動させる


# ボールの再描画
def redraw_ball(ball):    # ボールの再描写関数
    global canvas
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + ball.d, ball.y + ball.d)    # id の値を書き換える


# -------------------------
# paddle
# パドルの描画・登録
def make_paddle(x, y, w=100, h=20, c="blue"):    # パドル作成関数
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)    # id にパドルの初期値を保存
    return Paddle(id, x, y, w, h, 0, c)    # id を追加して返す


# パドルの移動(左右)
def move_paddle(pad):    # パドルの移動関数
    pad.x += pad.vx    # x を vx 分移動させる


# パドルの色を変える
def change_paddle_color(pad, c="red"):    # パドルの色を変える関数
    canvas.itemconfigure(pad.id, fill=c)    # fill を c にする
    canvas.itemconfigure(pad.id, outline=c)     # outline を c にする
    redraw_paddle(pad)    # パドル再描写


# パドルの再描画
def redraw_paddle(pad):    # パドルを再描写する関数
    canvas.coords(pad.id, pad.x, pad.y,
                  pad.x + pad.w, pad.y + pad.h)    # id の値を書き換える


# -------------------------
# パドル操作のイベントハンドラ
def left_paddle(event):  # 速度を左向き(マイナス)に設定
    paddle.vx = -PADDLE_VX    # パドルを左に動かす


def right_paddle(event):  # 速度を右向き(マイナス)に設定
    paddle.vx = PADDLE_VX    # パドルを右に動かす


def stop_paddle(event):  # 速度をゼロに設定
    paddle.vx = 0    # パドルを止める


# =================================================
tk = Tk()
tk.title("Game")

canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# -----------------
# 描画アイテムを準備する。
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)    # 実際にパドルを描写
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, 10)    # 実際にボールを描写
wall = Wall(WALL_X, WALL_Y, WALL_W, WALL_H)    # 実際に外枠を描写
make_wall(wall)    # 実際に壁を描写

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)    # 左押したら、パドルを左に動かす
canvas.bind_all('<KeyPress-Right>', right_paddle)    # 右押したら、パドルを右に動かす
canvas.bind_all('<KeyRelease-Left>', stop_paddle)    # 左離したら、パドルを止める
canvas.bind_all('<KeyRelease-Right>', stop_paddle)    # 左離したら、パドルを止める

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)  # パドルの移動
    move_ball(ball)  # ボールの移動
    if ball.x + ball.vx <= wall.x:  # 左側の壁を越えたら
        ball.vx = -ball.vx    # 反射させる
    if ball.x + ball.d + ball.vx >= wall.x + wall.w:  # 右の壁を越えたら
        ball.vx = -ball.vx    # 反射させる
    if ball.y + ball.vy <= wall.y:  # 上の壁を越えたら
        ball.vy = -ball.vy    # 反射させる
    if ball.y + ball.d + ball.vy >= 600:  # 下のキャンバスについたら
        break    # ループを抜ける（終了）
    if paddle.x <= 0:    # パドルがキャンバスの左についたら
        paddle.x = 0    # パドルを止める
    if paddle.x + paddle.w >= 800:    # パドルがキャンバスの右についたら
        paddle.x = 800 - paddle.w    # パドルを止める
    # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
    if (paddle.y <= ball.y + ball.d <= paddle.y + paddle.h \
            and paddle.x <= ball.x + ball.d / 2 <= paddle.x + paddle.w):    # パドルにボールが当たったら
        change_paddle_color(paddle, random.choice(COLORS))  # 色を変える
        ball.vy = -ball.vy  # ボールの移動方向が変わる

    redraw_paddle(paddle)  # パドルの再描画
    redraw_ball(ball)  # ボールの再描画
    tk.update()  # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleep する。

tk.mainloop()
