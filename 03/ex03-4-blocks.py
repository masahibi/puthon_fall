# 20K1026 日比野将己
# 練習問題 3-1-3
# --------------------------
# プログラム名: ex03-blocks.py

from tkinter import *
from dataclasses import dataclass
import random
import time

# 初期状態の設定
SPEEDS = [-3, -2, -1, 1, 2, 3, 4]  # ボールのx方向初速選択肢
BLOCKS_X = [150, 250, 350, 400]  # ブロックのｘ座標のリスト
BLOCKS_Y = [300, 100, 200, 300]  # ブロックのｙ座標のリスト
BLOCKS_W = [40, 40, 40, 40]  # ブロックの幅のリスト
BLOCKS_H = [30, 30, 30, 30]  # ブロックの高さのリスト
DURATION = 0.01  # 描画間隔(秒)
BALL_X0 = 400  # ボールの初期位置(x)
BALL_Y0 = 100  # ボールの初期位置(y)
PADDLE_X0 = 350  # パドルの初期位置(x)
PADDLE_Y0 = 500  # パドルの初期位置(y)
PADDLE_VX = 5  # パドルの速度
WALL_X0 = 100  # 外枠のｘ座標
WALL_Y0 = 50  # 外枠のｙ座標
WALL_W = 400  # 外枠の幅
WALL_H = 500  # 外枠の高さ

BALL_VX = random.choice(SPEEDS)  # ボールのx方向初速
BALL_VY = 0  # ボールのy方向初速

GRAVITY =0.05  # 重力加速度
REACTION = 1.01  # 反発係数

count1 = 0  # ブロックのx座標を判定する count
count2 = 0  # ブロックのｙ座標を判定する count

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

def make_wall(wall):  # 外枠を作る関数
    global canvas
    canvas.create_rectangle(wall.x, wall.y, wall.x + wall.w, wall.y + wall.h, width=10)  # 外枠
    canvas.create_line(WALL_X0, PADDLE_Y0, WALL_X0 + 50, PADDLE_Y0, width=10)  # パドルの左の出っ張り
    canvas.create_line(WALL_X0 + WALL_W, PADDLE_Y0, WALL_X0 + WALL_W - 50, PADDLE_Y0, width=10)  # パドルの右の出っ張り


def make_block(block, c="Blue"):  # ブロックを作る関数
    global canvas
    canvas.create_rectangle(block.x, block.y, block.x + block.w, block.y + block.h, fill=c, outline=c)  # ブロック作成


def block_judge(block):  # ブロックに当たったかを判定する関数
    global canvas
    if ball.x + ball.d > block.x and ball.x < block.x + block.w:  # もしブロックの上か下にボールがあれば
        count1 = 1  # count1 を１にする
    else:
        count1 = 0  # その他は 0
    if ball.y + ball.d > block.y and ball.y < block.y + block.h and count1 == 1:  # count1 が１で、ボールがブロックの上か下に当たれば
        ball.vy = -ball.vy  # ｙ方向に反射させる

    if ball.y + ball.d >= block.y and ball.y <= block.y + block.h:  # もしブロックの左か右にボールがあれば
        count2 = 1  # count2 を１にする
    else:
        count2 = 0  # その他は 0
    if ball.x + ball.d >= block.x and ball.x <= block.x + block.w and count2 == 1 and count1 != 1:  # count2 が１で、ボールがブロックの左か右に当たれば
        ball.vx = -ball.vx  # x 方向に反射させる

    # このようにそれぞれを完全に独立しておかないとお互い競合して vx と vy が両方変わって、当たったほうに戻っちゃう


# ball
# ボールの描画・登録
def make_ball(x, y, vx, vy, d=3, c="black"):  # ボールを作る関数
    global canvas
    id = canvas.create_oval(x, y, x + d, y + d,
                            fill=c, outline=c)  # 初期位置を id として保存
    return Ball(id, x, y, vx, vy, d, c)  # Ballクラスに id を加えて返す


# ボールの移動
def move_ball(ball):  # ボールの移動関数
    ball.x += ball.vx  # x 座標を vx 分移動させる
    ball.vy += GRAVITY  # vy に重力加速度を付加
    ball.y += ball.vy  # y 座標を vy 分移動させる


# ボールの再描画
def redraw_ball(ball):  # ボール再描写関数
    canvas.coords(ball.id, ball.x, ball.y,
                  ball.x + ball.d, ball.y + ball.d)  # id の値を書き換える


# -------------------------
# paddle
# パドルの描画・登録
def make_paddle(x, y, w=100, h=20, c="blue"):  # パドルを作る関数
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline=c)  # id に初期値を保存
    return Paddle(id, x, y, w, h, 0, c)  # パドルクラスに id をいれて返す


# パドルの移動(左右)
def move_paddle(pad):  # パドルの移動関数
    pad.x += pad.vx  # x 座標を vx 分移動させる


# パドルの色を変える
def change_paddle_color(pad, c="red"):  # パドルの色を変える関数
    canvas.itemconfigure(pad.id, fill=c)  # id の fill を c にする
    canvas.itemconfigure(pad.id, outline=c)  # id の outline を c にする
    redraw_paddle(pad)  # パドルを再描写する


# パドルの再描画
def redraw_paddle(pad):  # パドルの再描写関数
    canvas.coords(pad.id, pad.x, pad.y, pad.x + pad.w, pad.y + pad.h)  # id の値を書き換える


# -------------------------
# パドル操作のイベントハンドラ
def left_paddle(event):  # 速度を左向き(マイナス)に設定（左押された用）
    paddle.vx = -PADDLE_VX  # パドルを左に移動させる


def right_paddle(event):  # 速度を右向き(マイナス)に設定（右押された用）
    paddle.vx = PADDLE_VX  # パドルを右に移動させる


def stop_paddle(event):  # 速度をゼロに設定（何も押さない用）
    paddle.vx = 0  # パドルを止める


# =================================================
tk = Tk()
tk.title("Game")  # 左上のタイトルを書ける

canvas = Canvas(tk, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# -----------------
# 描画アイテムを準備する。
paddle = make_paddle(PADDLE_X0, PADDLE_Y0)  # パドル作成
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, 10)  # ボール作成
wall = Wall(WALL_X0, WALL_Y0, WALL_W, WALL_H)  # 外枠作成
make_wall(wall)  # 実際に外枠作成
blocks = []  # 作成されたブロックのリスト
for x in range(len(BLOCKS_X)):  # 4 回繰り返す（今回は４個ブロックを作るから）
    blocks.append(Block(BLOCKS_X[x], BLOCKS_Y[x], BLOCKS_W[x], BLOCKS_H[x]))  # blocks に作成されたブロックを追加
for block in blocks:  # blocks にあるblockを取ってくる
    make_block(block)  # 実際にブロック作成

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)  # Left 押したら left_paddle 実行
canvas.bind_all('<KeyPress-Right>', right_paddle)  # Right 押したら right_paddle 実行
canvas.bind_all('<KeyRelease-Left>', stop_paddle)  # Left 離したら stop_paddle 実行
canvas.bind_all('<KeyRelease-Right>', stop_paddle)  # Right 離したら stop_paddle 実行

# -------------------------
# プログラムのメインループ
while True:
    move_paddle(paddle)  # パドルの移動
    move_ball(ball)  # ボールの移動
    if ball.x + ball.vx <= wall.x:  # ボールが左枠を越えたら
        ball.vx = -ball.vx  # ボールを反射させる
    if ball.x + ball.d + ball.vx >= wall.x + wall.w:  # ボールが右枠を越えたら
        ball.vx = -ball.vx  # ボールを反射させる
    if ball.y + ball.vy <= wall.y:  # ボールが上枠を越えたら
        ball.vy = -ball.vy  # ボールを反射させる
    if ball.y + ball.d + ball.vy >= WALL_Y0 + WALL_H:  # ボールが下枠を越えたら
        break  # while を抜ける（終了）
    if paddle.x <= WALL_X0 + 50:  # パドルが左横の棒に当たったら
        paddle.x = WALL_X0 + 50  # パドルをその場に止める
    if paddle.x + paddle.w >= WALL_X0 + WALL_W - 50:  # パドルが右横の棒に当たったら
        paddle.x = WALL_X0 + WALL_W - 50 - paddle.w  # パドルをその場に止める
    # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
    if (paddle.y <= ball.y + ball.d <= paddle.y + paddle.h \
            and paddle.x <= ball.x + ball.d / 2 <= paddle.x + paddle.w):    # パドルにボールが当たったら
        change_paddle_color(paddle, random.choice(COLORS))  # 色を変える
        ball.vy = -ball.vy * REACTION  # ボールの移動方向が変わる（反射が大きくなる）
    if ball.x <= WALL_X0 + 50 and ball.y + ball.d >= PADDLE_Y0 \
            or ball.x >= WALL_X0 + WALL_W - 50 and ball.y + ball.d >= PADDLE_Y0:  # ボールが左の棒か右の棒に当たったら
        ball.vy = -ball.vy  # ボールを反射させる

    for x in range(len(BLOCKS_X)):    # 4 回繰り返す（今回は４つ作るから）
        block_judge(blocks[x])    # ボールがブロックに当たったら跳ね返す

    redraw_paddle(paddle)  # パドルの再描画
    redraw_ball(ball)  # ボールの再描画
    tk.update()  # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleep する。

tk.mainloop()
