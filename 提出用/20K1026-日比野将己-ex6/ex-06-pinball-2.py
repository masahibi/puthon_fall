# 20K1026 日比野将己
# 第６回 - 課題[2]
# --------------------------
# プログラム名: ex-06-pinball-2.py

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
PADDLE_START_POS = 80  # パドルの最初の位置

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
        self.y += self.vy  # ｙ方向に移動

    def redraw(self):  # ボールの再描画関数
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.d, self.y + self.d)  # idの座標を変更


class Paddle:
    def __init__(self, id, x, y, w, h, dx=0):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = dx

    def move(self):  # パドルの移動関数
        self.x += self.dx  # x方向に移動

    def redraw(self):  # パドルの再描画関数
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)  # idの座標を変更


class Box:
    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.ball = None  # 後で使う場合はとりあえずNone
        self.duration = duration
        self.paddle = None
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white")

    def create_ball(self, x, y, d, vy):  # ボール作成関数
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")  # 初期描写
        return Ball(id, x, y, d, vy)  # ボールクラスを生成して返す

    def set_balls(self):  # ボールの描写関数（いい感じの説明が思いつかなかった）
        self.ball = self.create_ball(BALL_INITIAL_X,
                                     BALL_INITIAL_Y + BALL_DIAMETER,
                                     BALL_DIAMETER, BALL_SPEED)  # ボールクラス代入

    def create_paddle(self, x, y, w, h):  # パドル作成関数
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")  # 初期描写
        return Paddle(id, x, y, w, h)  # パドルクラスを生成して返す

    def set_paddle(self):  # パドルの描写関数（いい感じの説明が思いつかなかった）
        self.paddle = self.create_paddle(
            self.west + PADDLE_START_POS,
            self.south - PADDLE_HEIGHT,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )  # パドルクラス代入

    def check_wall(self):  # 壁の判定関数
        if self.ball.y <= self.north:  # もし上壁を越えたら
            self.ball.vy = - self.ball.vy  # 跳ね返す

    def check_paddle(self):  # パドルの判定関数
        if self.ball.x + self.ball.d >= self.paddle.x \
                and self.ball.x <= self.paddle.x + self.paddle.w \
                and self.ball.y + self.ball.d >= self.paddle.y:  # もしパドルに当たったら
            self.ball.vy = - self.ball.vy  # 跳ね返す
            self.ball.y = self.paddle.y - self.ball.d  # ボールをパドルの位置にする

    def left_paddle(self, event):  # 左のイベント関数
        self.paddle.dx = -10  # 左に移動

    def right_paddle(self, event):  # 右のイベント関数
        self.paddle.dx = 10  # 右に移動

    def stop_paddle(self, event):  # 離したときのイベント関数
        self.paddle.dx = 0  # ストップ

    def animate(self):  # アニメーション関数
        while True:
            self.ball.move()  # ボール移動
            self.check_wall()  # 壁の判定
            self.check_paddle()  # パドルの判定
            self.ball.redraw()  # ボールの再描写
            self.paddle.move()  # パドル移動
            self.paddle.redraw()  # パドルの再描写
            if self.ball.y + self.ball.d >= self.south:  # もし下に当たったら  ←-- 関数にするとbreakが使えないから、これは直接！
                break  # 終了
            time.sleep(self.duration)
            tk.update()


# main
tk = Tk()
canvas = Canvas(tk, width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT, bd=0)
canvas.pack()

box = Box(BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT, duration=DURATION)  # ボールクラス生成
canvas.bind_all('<KeyPress-Left>', box.left_paddle)  # 左押したら、パドルを左に
canvas.bind_all('<KeyPress-Right>', box.right_paddle)  # 右押したら、パドルを右に
canvas.bind_all('<KeyRelease-Left>', box.stop_paddle)  # 左離したら、パドルストップ
canvas.bind_all('<KeyRelease-Right>', box.stop_paddle)  # 右離したら、パドルストップ
box.set_balls()  # ボールの初期描写
box.set_paddle()  # パドルの初期描写
box.animate()  # アニメーション(実行)
tk.mainloop()
