from tkinter import *
from dataclasses import dataclass
import time

DURATION = 0.005  # 画面停止時間
GRAVITY = 0.1  # 重力
REACTION = 0.9  # 弾性力
y1 = 1  # 頂点のy座標
y2 = 1000  # 着地した時のｙ座標
count = 0


@dataclass
class Ball:  # ボールのクラス
    id: float
    x: float  # x 座標
    y: float  # y 座標
    d: float  # 大きさ
    vx: float  # x 軸の初速
    vy: float  # y 軸の初速
    c: str


@dataclass
class Border:  # 枠線のクラス
    left: int  # 左枠の位置
    right: int  # 右枠の位置
    top: int  # 上枠の位置
    bottom: int  # 下枠の位置


def make_wall(x, y, w, h):  # 外枠の作成
    global canvas
    canvas.create_rectangle(x, y, x + w, y + h)  # 四角書くやつ


def make_ball(x, y, d, vx, vy, c="black"):  # ボール１つ作成
    global canvas
    id = canvas.create_rectangle(x, y, x + d, y + d, outline=c, fill=c)  # 四角情報取得
    return Ball(id, x, y, d, vx, vy, c)  # ボールクラスの値を更新して返す


def move_ball(ball):  # 座標の移動
    ball.x += ball.vx  # x軸方向の移動
    ball.y += ball.vy  # y軸方向の移動


def redraw_ball(ball):  # 移動後のボールの描写
    global canvas
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + ball.d, ball.y + ball.d)  # id の座標の変更


tk = Tk()
canvas = Canvas(tk, width=800, height=600)
canvas.pack()
tk.update()

border = Border(100, 700, 100, 500)  # 枠線のクラス作成
make_wall(border.left, border.top,
          border.right - border.left, border.bottom - border.top)  # 枠線の描写

# balls = [
# make_ball(100, 100, 20, 2, 1, "darkblue"),
# make_ball(200, 200, 25, -4, 3, "orange"),
# make_ball(300, 300, 10, -2, -1, "green"),
# make_ball(400, 400, 5, 4, 2, "darkgreen")
# ]
ball = make_ball(200, 200, 50, 3, 0, "black")

while True:
    # for ball in balls:
    if y2 - y1 < sys.float_info.min:  # 頂点と着地の y 座標の差が限りなく 0 に近づいたとき（完全な方法を思いつかなかった）
        continue  # ループを飛ばす
    ball.vy += GRAVITY  # 重力付加
    move_ball(ball)  # ボール動かす

    under_ball = ball.y + ball.d    # ボールの下
    right_ball = ball.x + ball.d    # ボールの右

    if ball.x <= border.left or \
            right_ball >= border.right:  # 左枠か右枠を超えたら
        ball.vx = -ball.vx  # 向きを逆にする

    if ball.y + ball.vy < border.top \
            or ball.y + ball.d >= border.bottom:  # 下線をボールが越えたら
        ball.vy *= -REACTION  # 逆方向にボールを反射させる
        y2 = ball.y  # y 座標取得
        count = 0  # countを元に戻す

    if ball.vy > 0 and count == 0:  # 頂点に来た時
        y1 = ball.y  # y 座標取得
        count = 1  # 一回だけにしたいため、+1

    redraw_ball(ball)  # 動いた後を描写
    tk.update()  # 画面更新
    time.sleep(DURATION)  # 0.001秒処理停止

# canvas.mainloop()
