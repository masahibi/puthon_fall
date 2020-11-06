# Python によるプログラミング：第 6 章
#  練習問題 6.1 Paddleクラスの実装
# --------------------------
# プログラム名: ex06-block-1.py

from tkinter import *
from dataclasses import dataclass, field
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

DURATION = 0.05  # アニメーションのスピード

PADDLE_WIDTH = 50  # パドルの幅
PADDLE_HEIGHT = 10  # パドルの高さ
PADDLE_START_POS = 80  # パドルの最初の位置

CANVAS_WIDTH = BOX_LEFT + BOX_WIDTH + 100  # キャンバスの大きさ
CANVAS_HEIGHT = BOX_TOP + BOX_HEIGHT + 100

GRAVITY = 0.5


@dataclass
class Ball:
    id: int
    x: int
    y: int
    d: int
    vy: int

    def move(self):  # ボールを動かす
        self.vy += GRAVITY
        self.y += self.vy

    def redraw(self):  # ボールの再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)


@dataclass
class Paddle:
    id: int
    x: int
    y: int
    w: int
    h: int
    dy: int = field(init=False, default=0)

    def move(self):  # パドルを動かす
        self.y += self.dy

    def redraw(self):  # パドルの再描画
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)


@dataclass
class Box:
    id: int
    west: int
    north: int
    east: int
    south: int
    balls: list
    duration: float
    paddle: Paddle

    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.ball = None
        self.duration = duration
        self.paddle = None
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white")

    def create_ball(self, x, y, d, vy):  # ボールを生成し、初期描画する
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")
        return Ball(id, x, y, d, vy)

    def set_balls(self):
        # for x in range(n):
        self.ball = self.create_ball(BALL_INITIAL_X,
                                BALL_INITIAL_Y + BALL_DIAMETER,
                                BALL_DIAMETER, BALL_SPEED)
            # self.balls.append(ball)

    def create_paddle(self, x, y, w, h):
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")
        return Paddle(id, x, y, w, h)

    def set_paddle(self):
        self.paddle = self.create_paddle(
            self.west + PADDLE_START_POS,
            self.south - PADDLE_HEIGHT,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )

    def check_wall(self):
        if self.ball.y <= self.north:
            self.ball.vy = - self.ball.vy

    def check_paddle(self):
        if self.ball.x + self.ball.d >= self.paddle.x and self.ball.x <= self.paddle.x + self.paddle.w and self.ball.y + self.ball.d >= self.paddle.y:
            self.ball.vy = - self.ball.vy
            self.ball.y = self.paddle.y - self.ball.d

    def animate(self):
        # for x in range(100):  # iterate 100 times
        while True:
            # for ball in self.balls:
            self.ball.move()
            self.check_wall()
            self.check_paddle()
            self.ball.redraw()
            self.paddle.move()
            self.paddle.redraw()
            time.sleep(self.duration)
            tk.update()


# main
tk = Tk()
canvas = Canvas(tk, width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT, bd=0)
canvas.pack()

box = Box(BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT, duration=DURATION)    # ボールクラス生成

box.set_balls()    # ボールの初期描写
box.set_paddle()    # パドルの初期描写
box.animate()    # アニメーション(実行)
