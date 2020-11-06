# 20K1026 日比野将己
# 課題 [1]
# --------------------------
# プログラム名: ex06-pinball-1.py

from tkinter import *
import time

# 定数定義
BOX_LEFT = 100  # ゲーム領域の左端
BOX_TOP = 100  # ゲーム領域の上位置
BOX_WIDTH = 300  # ゲーム領域の幅
BOX_HEIGHT = 300  # ゲーム領域の高さ

BALL_INITIAL_X = BOX_LEFT + 100  # ボールの最初のX位置
BALL_INITIAL_Y = BOX_TOP + 20  # ボールの最初のY位置
BALL_DIAMETER = 10  # ボールの直径
BALL_SPEED = 5  # ボールのスピード

DURATION = 0.03  # アニメーションのスピード

PADDLE_WIDTH = 50  # パドルの幅
PADDLE_HEIGHT = 10  # パドルの高さ
PADDLE_START_POS = 70  # パドルの最初の位置

CANVAS_WIDTH = BOX_LEFT + BOX_WIDTH + 100  # キャンバスの大きさ
CANVAS_HEIGHT = BOX_TOP + BOX_HEIGHT + 100

GRAVITY = 0.5  # 重力


class Ball:
    def __init__(self, id, x, y, d, vy):
        self.id = id
        self.x = x
        self.y = y
        self.d = d
        self.vy = vy

    def move(self):  # ボールの移動関数
        self.vy += GRAVITY  # 重力付与
        self.y += self.vy  # ｙ方向移動

    def redraw(self):  # ボールの再描画関数
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)  # idの座標変更


class Paddle:
    def __init__(self, id, x, y, w, h, dy=0):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dy = dy


class Box:
    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.ball = None  # 今後出てくるときはとりあえずNone
        self.duration = duration
        self.paddle = None
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white")

    def create_ball(self, x, y, d, vy):  # ボール作成関数
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")  # ボール描写
        return Ball(id, x, y, d, vy)  # クラス生成を返す

    def set_balls(self):  # ボール描写関数（いい感じの説明が思いつかなかった）
        self.ball = self.create_ball(BALL_INITIAL_X,
                                     BALL_INITIAL_Y + BALL_DIAMETER,
                                     BALL_DIAMETER, BALL_SPEED)  # ボールクラス代入

    def create_paddle(self, x, y, w, h):  # パドル作成関数
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")  # パドル描写
        return Paddle(id, x, y, w, h)  # クラス生成を返す

    def set_paddle(self):  # パドル描写関数（いい感じの説明が思いつかなかった）
        self.paddle = self.create_paddle(
            self.west + PADDLE_START_POS,
            self.south - PADDLE_HEIGHT,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )  # パドルクラス代入

    def check_wall(self):  # 壁の判定関数
        if self.ball.y <= self.north:  # 上の壁を越えたら
            self.ball.vy = - self.ball.vy  # 跳ね返す

    def check_paddle(self):  # パドルの判定関数
        if self.ball.x + self.ball.d >= self.paddle.x \
                and self.ball.x <= self.paddle.x + self.paddle.w \
                and self.ball.y + self.ball.d >= self.paddle.y:  # パドルに当たったら
            self.ball.vy = - self.ball.vy  # 跳ね返す
            self.ball.y = self.paddle.y - self.ball.d  # ボールをパドルの上にする

    def animate(self):  # アニメーション関数
        while True:
            self.ball.move()  # ボール移動
            self.check_wall()  # 壁の判定
            self.check_paddle()  # パドルの判定
            self.ball.redraw()  # ボールの再描写
            time.sleep(self.duration)
            tk.update()


# main
tk = Tk()
canvas = Canvas(tk, width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT, bd=0)
canvas.pack()

box = Box(BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT, duration=DURATION)  # ボールクラス生成

box.set_balls()  # ボールの初期描写
box.set_paddle()  # パドルの初期描写
box.animate()  # アニメーション(実行)
tk.mainloop()
