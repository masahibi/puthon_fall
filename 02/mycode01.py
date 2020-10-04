from tkinter import *
from dataclasses import dataclass
import time

DURATION = 0.01    # 画面停止時間
GRAVITY = 0.1    # 重力
REACTION = 0.9   # 弾性力


@dataclass
class Ball:    # ボールのクラス
    id: float
    x: float  # x 座標
    y: float  # y 座標
    d: float  # 大きさ
    vx: float  # x 軸の初速
    vy: float  # y 軸の初速
    c: str


@dataclass
class Border:    # 枠線のクラス
    left: int    # 左枠の位置
    right: int    # 右枠の位置
    top: int    # 上枠の位置
    bottom: int    # 下枠の位置


def make_wall(x, y, w, h):    # 外枠の作成
    global canvas
    canvas.create_rectangle(x, y, x + w, y + h)    # 四角書くやつ


def make_ball(x, y, d, vx, vy, c="black"):    # ボール１つ作成
    global canvas
    id = canvas.create_rectangle(x, y, x + d, y + d, outline=c, fill=c)    # 四角作成
    return Ball(id, x, y, d, vx, vy, c)    # ボールクラスの値を更新して返す


def move_ball(ball):    # 座標の移動
    ball.x += ball.vx    # x軸方向の移動
    ball.y += ball.vy    # y軸方向の移動


def redraw_ball(ball):    # 移動後のボールの描写
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + ball.d, ball.y + ball.d)    # id の座標の変更


tk = Tk()
canvas = Canvas(tk, width=800, height=600)
canvas.pack()
tk.update()

border = Border(100, 700, 100, 500)    # 枠線のクラス作成
make_wall(border.left, border.top, border.right - border.left, border.bottom - border.top)    # 枠線の描写

balls = [
    make_ball(100, 100, 20, 2, 1, "darkblue"),
    make_ball(200, 200, 25, -4, 3, "orange"),
    make_ball(300, 300, 10, -2, -1, "green"),
    make_ball(400, 400, 5, 4, 2, "darkgreen")
    ]

while True:
    for ball in balls:
        ball.vy += GRAVITY    # 重力付加
        move_ball(ball)    # ボール動かす

        under_ball = ball.y + ball.d
        right_ball = ball.x + ball.d

        if ball.x <= border.left or right_ball >= border.right:
            ball.vx = -ball.vx

        if under_ball >= border.bottom:    # 下線をボールが越えたら
            ball.vy *= -REACTION    # 逆方向にボールを反射させる
            under_ball = border.bottom    # ボールが越えないように、下線の位置にする

        redraw_ball(ball)    # 動いた後を描写

    tk.update()    # 画面更新
    time.sleep(DURATION)    # 0.001秒処理停止

# canvas.mainloop()
