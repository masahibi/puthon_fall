# 20K1026 日比野将己
# 第１回　レポート課題プログラム
# --------------------------
# プログラム名: 20K1026-日比野将己-r01.py

from tkinter import *
from dataclasses import dataclass
import random
import time

# 初期状態の設定
SPEEDS = [-2, -1, 1, 2]  # ボールのx方向初速選択肢
BLOCKS_X = [150, 250, 350, 400]  # ブロックのｘ座標のリスト
random.shuffle(BLOCKS_X)
BLOCKS_Y = [100, 200, 300, 350]  # ブロックのｙ座標のリスト
random.shuffle(BLOCKS_Y)
BLOCKS_W = [40, 40, 40, 40]  # ブロックの幅のリスト
BLOCKS_H = [20, 20, 20, 20]  # ブロックの高さのリスト
DURATION = 0.01  # 描画間隔(秒)
BALL_X0 = 470  # ボールの初期位置(x)
BALL_Y0 = 550  # ボールの初期位置(y)
PADDLE_X0 = 350  # パドルの初期位置(x)
PADDLE_Y0 = 500  # パドルの初期位置(y)
PADDLE_VX = 5  # パドルの速度
WALL_X0 = 100  # 外枠のｘ座標
WALL_Y0 = 80  # 外枠のｙ座標
WALL_W = 400  # 外枠の幅
WALL_H = 500  # 外枠の高さ

BALL_VX = random.choice(SPEEDS)  # ボールのx方向初速
BALL_VY = -10   # ボールのy方向初速

GRAVITY = 0.11  # 重力加速度
REACTION = 0.99  # 反発係数

count1 = 0  # ブロックのx座標を判定する count
count2 = 0  # ブロックのｙ座標を判定する count
count3 = 0  # play_start
count4 = 0  # db からダウンロード

play = 0
score = 0
select_x = 150
select_y = 170
select_w = 300
select_h = 80
c = 0  # パドルの色

blocks = []  # 作成されたブロックのリスト

# 変える色を用意する。
COLORS = ["#1f0000", "#3f0000", "#5f0000", "#7f0000", "#9f0000", "#bf0000", "#df0000", "#ff0000"]


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
    id: int
    x: int
    y: int
    w: int
    h: int
    c: str


@dataclass
class Point:
    id: int
    x: int
    y: int
    score: int


@dataclass
class Select:
    id: int
    y: int


# -------------------------

def make_wall(wall):  # 外枠を作る関数
    global canvas
    canvas.create_rectangle(wall.x, wall.y, wall.x + wall.w, wall.y + wall.h, width=10, outline="white")  # 外枠
    # canvas.create_line(wall.x, PADDLE_Y0, wall.x + 50, PADDLE_Y0, width=10, fill="white")  # パドルの左の出っ張り
    # canvas.create_line(wall.x + wall.w - 50, PADDLE_Y0, wall.x + wall.w - 100, PADDLE_Y0, width=10,
    #                    fill="white")  # パドルの右の出っ張り
    canvas.create_line(wall.x + wall.w - 50, wall.y + 150, wall.x + wall.w - 50, wall.y + wall.h, width=10,
                       fill="white")  # 縦線
    canvas.create_line(wall.x + wall.w - 100, wall.y, wall.x + wall.w, wall.y + 50, width=10, fill="white")  # 右上斜め
    canvas.create_line(wall.x, paddle1.y - 50, wall.x + 80, paddle1.y, width=10, fill="white")  # 左下斜め
    canvas.create_line(wall.x + wall.w - 130, paddle1.y, wall.x + wall.w - 50, paddle1.y - 50, width=10,
                       fill="white")  # 右下斜め


# ブロックの描画
def make_block(x, y, w, h, c="blue"):
    id = canvas.create_rectangle(x, y, x + w, y + h, fill=c, outline="white")
    return Block(id, x, y, w, h, c)


# ブロックの消去
def delete_block(block):
    global blocks
    canvas.delete(block.id)
    blocks.remove(block)


# ブロックをまとめて描画
def make_blocks(x, y, w, h):
    blocks = []
    for i in range(len(x)):
        blocks.append(make_block(x[i], y[i], w[i], h[i]))
    return blocks


def block_judge(block):  # ブロックに当たったかを判定する関数
    global canvas, count1, count2, score
    if ball.x + ball.d > block.x and ball.x < block.x + block.w:  # もしブロックの上か下にボールがあれば
        count1 = 1  # count1 を１にする
    else:
        count1 = 0  # その他は 0
    if ball.y + ball.d > block.y and ball.y < block.y + block.h and count1 == 1:  # count1 が１で、ボールがブロックの上か下に当たれば
        ball.vy = -ball.vy  # ｙ方向に反射させる
        count1 = 2

    if ball.y + ball.d >= block.y and ball.y <= block.y + block.h:  # もしブロックの左か右にボールがあれば
        count2 = 1  # count2 を１にする
    else:
        count2 = 0  # その他は 0
    if ball.x + ball.d >= block.x and ball.x <= block.x + block.w and count2 == 2:  # count2 が１で、ボールがブロックの左か右に当たれば
        ball.vx = -ball.vx  # x 方向に反射させる
        count2 = 2

    if count1 == 2 or count2 == 2:  # ブロックに当たれば
        delete_block(block)  # ブロックを消す
        score += 10  # スコアを加算する
        redraw_point()  # ポイントを書き換える
    # このようにそれぞれを完全に独立しておかないとお互い競合して vx と vy が両方変わって、当たったほうに戻っちゃう


# ball
# ボールの描画・登録
def make_ball(x, y, vx, vy, d=3, c="white"):  # ボールを作る関数
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
def make_paddle(x, y, w=100, h=10, c="white"):  # パドルを作る関数
    id = canvas.create_rectangle(x, y, x + w, y + h,
                                 fill=c, outline="white")  # id に初期値を保存
    return Paddle(id, x, y, w, h, 0, c)  # パドルクラスに id をいれて返す


# パドルの移動(左右)
def move_paddle(pad):  # パドルの移動関数
    pad.x += pad.vx  # x 座標を vx 分移動させる


# パドルの色を変える
def change_paddle_color(pad, c):  # パドルの色を変える関数
    canvas.itemconfigure(pad.id, fill=c)  # id の fill を c にする
    canvas.itemconfigure(pad.id, outline="white")  # id の outline を c にする
    redraw_paddle(pad)  # パドルを再描写する


# パドルの再描画
def redraw_paddle(pad):  # パドルの再描写関数
    global canvas
    canvas.coords(pad.id, pad.x, pad.y, pad.x + pad.w, pad.y + pad.h)  # id の値を書き換える


# -------------------------
# パドル操作のイベントハンドラ
def left_paddle(event):  # 速度を左向き(マイナス)に設定（左押された用）
    paddle1.x = wall.x + 80  # パドルを左に移動させる


def right_paddle(event):  # 速度を右向き(マイナス)に設定（右押された用）
    paddle2.x = 200


def stop_paddle(event):  # 速度をゼロに設定（何も押さない用）
    paddle1.x = wall.x  # パドルを止める


def play_start(event):
    global play, count3, start_rect, start_text
    if count3 == 0:
        canvas.delete(start_rect, start_text)
        count3 = 1
    elif count3 == 1:
        canvas.delete(select_rect1, select_rect2, select_text1, select_text2)
        count3 =2
    else:
        play = 1


def select_up(event):
    select.y = 170
    redraw_select(select)


def select_down(event):
    global select_y
    select.y = 260
    redraw_select(select)
    select_y = select.y


# -------------------------
# その他
def draw_point(score):
    global canvas, point
    canvas.create_rectangle(20, 20, 150, 50, width=3, fill="lightgrey")
    id = canvas.create_text(75, 38, text=f"score：{score}", font=("", 15, "bold"))
    return id


def redraw_point():  # パドルの再描写関数
    global canvas, point
    canvas.delete(point)
    point = canvas.create_text(75, 38, text=f"score：{score}", font=("", 15, "bold"))  # coords は座標しか変えれない


def start():
    global canvas, start_rect, start_text
    start_rect = canvas.create_rectangle(40, 150, 560, 350, fill="lightgrey", width=2)
    start_text = canvas.create_text(300, 250, text="START\n(space)", font=("", 50, "bold"))


def select_score(y):
    global canvas, select_rect1, select_rect2, select_text1, select_text2
    select_rect1 = canvas.create_rectangle(40, 150, 560, 350, fill="lightgrey", width=2)
    select_rect2 = canvas.create_rectangle(150, y, 150 + 300, y + 80, width=5)
    select_text1 = canvas.create_text(300, 210, text="最初から", font=("", 50, "bold"))
    select_text2 = canvas.create_text(300, 300, text="続きから", font=("", 50, "bold"))
    return Select(select_rect2, y)


def redraw_select(select):
    global canvas
    canvas.coords(select.id, 150, select.y, 150 + 300, select.y + 80)  # id の値を書き換える


def finish():
    global canvas
    if ball.y + ball.d + ball.vy >= wall.y + wall.h or len(blocks) == 0 or c == 8:  # ボールが下枠を越えたら
        if select_y == 260:
            with open(r"db.txt", mode="w") as file:
                file.write(str(score))
        if len(blocks) == 0:
            canvas.create_text(300, 300, text="CLEAR!!", font=("", 50, "bold"), fill="green")
        else:
            canvas.create_text(300, 300, text="～GAME OVER～", font=("", 50, "bold"), fill="red")


# =================================================
tk = Tk()
tk.title("Game")  # 左上のタイトルを書ける

canvas = Canvas(tk, width=600, height=700, bg="black", highlightthickness=0)
canvas.pack()
tk.update()

# -----------------
# 描画アイテムを準備する。
paddle1 = make_paddle(PADDLE_X0, PADDLE_Y0)  # パドル作成
paddle2 = make_paddle(PADDLE_X0, PADDLE_Y0)  # パドル作成
ball = make_ball(BALL_X0, BALL_Y0, BALL_VX, BALL_VY, 10)  # ボール作成
wall = Wall(WALL_X0, WALL_Y0, WALL_W, WALL_H)  # 外枠作成
make_wall(wall)  # 実際に外枠作成
blocks = make_blocks(BLOCKS_X, BLOCKS_Y, BLOCKS_W, BLOCKS_H)  # ブロック作成
point = draw_point(score)
select = select_score(select_y)
start()

# イベントと、イベントハンドラを連結する。
canvas.bind_all('<KeyPress-Left>', left_paddle)  # Left 押したら left_paddle 実行
canvas.bind_all('<KeyPress-Right>', right_paddle)  # Right 押したら right_paddle 実行
canvas.bind_all('<KeyRelease-Left>', stop_paddle)  # Left 離したら stop_paddle 実行
canvas.bind_all('<KeyRelease-Right>', stop_paddle)  # Right 離したら stop_paddle 実行
canvas.bind_all('<KeyPress-space>', play_start)  # Right 離したら stop_paddle 実行
canvas.bind_all('<KeyPress-Up>', select_up)  # Right 離したら stop_paddle 実行
canvas.bind_all('<KeyPress-Down>', select_down)  # Right 離したら stop_paddle 実行

# -------------------------
# プログラムのメインループ
while True:

    move_paddle(paddle1)  # パドルの移動
    move_paddle(paddle2)  # パドルの移動
    if paddle1.x <= wall.x:  # パドルが左横の棒に当たったら
        paddle1.x = wall.x  # パドルをその場に止める
    if paddle1.x + paddle1.w >= wall.x + wall.w - 50:  # パドルが右横の棒に当たったら
        paddle1.x = wall.x + wall.w - 50 - paddle1.w  # パドルをその場に止める

    if play == 0:
        redraw_paddle(paddle1)  # パドルの再描画
        tk.update()  # 描画が画面に反映される。
        time.sleep(DURATION)  # 次に描画するまで、sleep する。
        continue

    if select_y == 260 and count4 == 0:
        with open(r"db.txt") as file:
            score = int(file.readline())
            redraw_point()
        count4 = 1

    move_ball(ball)  # ボールの移動
    if ball.x + ball.vx <= wall.x:  # ボールが左枠を越えたら
        ball.vx = -ball.vx  # ボールを反射させる
    if ball.x + ball.d + ball.vx >= wall.x + wall.w:  # ボールが右枠を越えたら
        ball.vx = -ball.vx  # ボールを反射させる
    if ball.y + ball.vy <= wall.y:  # ボールが上枠を越えたら
        ball.vy = -ball.vy  # ボールを反射させる
    if wall.x + wall.w - 50 >= ball.x >= wall.x + wall.w - 52 and ball.y >= wall.y + 150:  # 縦線で跳ね返る
        ball.vx = -ball.vx
    if wall.x + wall.w - 100 <= ball.x <= wall.x + wall.w and wall.y <= ball.y <= wall.y + 50 and ball.y <= (1/2) * ball.x - 120:    # 右上斜めで跳ね返る
        ball.vy = -ball.vy
        ball.vx = -abs(ball.vx)
    if wall.x <= ball.x <= wall.x + 80 and paddle1.y - 50 <= ball.y + ball.d <= paddle1.y and ball.y + ball.d >= (5/8) * ball.x + 387.5:    # 左下斜めで跳ね返る
        ball.vy = -ball.vy
        ball.y = (5 / 8) * ball.x + 387.5 - ball.d

    if wall.x + wall.w - 130 <= ball.x + ball.d <= wall.x + wall.w - 50 and paddle1.y - 50 <= ball.y + ball.d <= paddle1.y and ball.y + ball.d >= -(5/8) * ball.x + ball.d + 731.25:    #右下斜めで跳ね返る
        ball.vy = -ball.vy
        ball.y = -(5 / 8) * ball.x + ball.d + 731.25 - ball.d

    if ball.y + ball.d + ball.vy >= wall.y + wall.h or len(blocks) == 0 or c == 8:  # ボールが下枠を越えたら
        if select_y == 260:
            with open(r"db.txt", mode="w") as file:
                file.write(str(score))
        finish()
        break  # while を抜ける（終了）

    # ボールの下側がパドルの上面に届き、横位置がパドルと重なる
    if (paddle1.y <= ball.y + ball.d <= paddle1.y + paddle1.h \
            and paddle1.x <= ball.x + ball.d / 2 <= paddle1.x + paddle1.w):  # パドルにボールが当たったら
        change_paddle_color(paddle1, COLORS[c])  # だんだん赤くなる
        c += 1
        ball.vy = -ball.vy * REACTION  # ボールの移動方向が変わる（反射が大きくなる）
        ball.y = paddle1.y - ball.d

    if ball.x <= wall.x + 50 and ball.y + ball.d >= paddle1.y \
            or ball.x >= wall.x + wall.w - 100 and ball.y + ball.d >= paddle1.y:  # ボールが左の棒か右の棒に当たったら
        ball.vy = -ball.vy  # ボールを反射させる
        ball.y = paddle1.y - ball.d

    for block in blocks:  # 4 回繰り返す（今回は４つ作るから）
        block_judge(block)  # ボールがブロックに当たったら跳ね返す

    redraw_paddle(paddle1)  # パドルの再描画
    redraw_paddle(paddle2)  # パドルの再描画

    redraw_ball(ball)  # ボールの再描画
    tk.update()  # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleep する。

tk.mainloop()
