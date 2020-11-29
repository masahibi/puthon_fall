# 20K1026 日比野将己
#  第7回-課題[2]
# --------------------------
# プログラム名: ex-07-pinball-polymorphic.py

from tkinter import *
import time
import random

# 定数定義
BOX_LEFT = 100  # ゲーム領域の左端
BOX_TOP = 100  # ゲーム領域の上位置
BOX_WIDTH = 300  # ゲーム領域の幅
BOX_HEIGHT = 400  # ゲーム領域の高さ

# BALL_INITIAL_X = BOX_LEFT + 100  # ボールの最初のX位置
BALL_INITIAL_X = BOX_LEFT + 270  # ボールの最初のX位置
BALL_INITIAL_Y = BOX_TOP + 350  # ボールの最初のY位置
BALL_DIAMETER = 10  # ボールの直径
BALL_Y_SPEED = -20  # ボールのスピード
BALL_X_SPEEDS = [-4, -3, 3, 4]
BALL_X_SPEED = random.choice(BALL_X_SPEEDS)

BLOCKS_X = [120, 180, 240, 290]  # ブロックのｘ座標のリスト
BLOCKS_Y = [110, 200, 300, 350]  # ブロックのｙ座標のリスト
BLOCK_W = 50
BLOCK_H = 10

DURATION = 0.03  # アニメーションのスピード

PADDLE_WIDTH = 70  # パドルの幅
PADDLE_HEIGHT = 10  # パドルの高さ
PADDLE_START_POS = 80  # パドルの最初の位置

CANVAS_WIDTH = BOX_LEFT + BOX_WIDTH + 100  # キャンバスの大きさ
CANVAS_HEIGHT = BOX_TOP + BOX_HEIGHT + 100

GRAVITY = 0.5  # 重力
REACTION = 1.005

PLUNGER_WIDTH = 50
PLUNGER_HEIGHT = 100

SCORE_RECT_X = 20
SCORE_RECT_Y = 20
SCORE_RECT_W = 130
SCORE_RECT_H = 30

SCORE_X = SCORE_RECT_X + 10
SCORE_Y = SCORE_RECT_Y + 15

START_RECT_X = BOX_LEFT - 70
START_RECT_Y = BOX_TOP + 50
START_RECT_W = 450
START_RECT_H = 200

SELECT_X = START_RECT_X + 50
SELECT_Y = START_RECT_Y + 20
SELECT_W = 350
SELECT_H = 80

TEXT_X = SELECT_X + 50
TEXT_Y = SELECT_Y + 70

blocks = []  # ブロックリスト
walls = []

start_count = 0
select_count = 0
score = 0


class MovingObject:  # ボール、パドル、ブロックの親クラス
    def __init__(self, id, x, y, w, h, vx, vy):
        self.id = id
        self.x, self.y = (x, y)
        self.w, self.h = (w, h)
        self.vx, self.vy = (vx, vy)

    def move(self):  # 共通の移動関数
        pass

    def redraw(self):  # 共通の再描写関数
        canvas.coords(self.id, self.x, self.y,
                      self.x + self.w, self.y + self.h)  # id の座標を変更


class Block(MovingObject):  # MovingObject の子クラス
    def __init__(self, id, x, y, w, h):
        MovingObject.__init__(self, id, x, y, w, h, 0, 0)  # 親クラスの継承


class Ball(MovingObject):  # MovingObject の子クラス
    def __init__(self, id, x, y, d, vx, vy):
        MovingObject.__init__(self, id, x, y, d, d, vx, vy)  # 親クラスの継承
        self.d = d

    def move(self):  # ボールの移動関数
        self.x += self.vx
        self.vy += GRAVITY  # 重力付与
        self.y += self.vy  # 移動させる


class Paddle(MovingObject):  # MovingObject の子クラス
    def __init__(self, id, x, y, w, h, dx=0):
        MovingObject.__init__(self, id, x, y, w, h, dx, 0)  # 親クラスの継承
        self.dx = dx

    def move(self):  # パドルの移動関数
        self.x += self.dx  # x方向に移動


class Wall:
    def __init__(self, id, x1, y1, x2, y2):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Score:
    def __init__(self, id):
        self.id = id

    def redraw(self):
        canvas.delete(point.id)  # スコアの描写を消す
        point.id = canvas.create_text(SCORE_X, SCORE_Y, text=f"score：{score}", font=("", 15, "bold"), anchor="w")
        # pointオブジェクトのidを変更　　coords は座標しか変えれない


class Select(MovingObject):
    def __init__(self, id, x, y, w, h):
        MovingObject.__init__(self, id, x, y, w, h, 0, 0)  # 親クラスの継承

    def move(self):
        if select_count == 0:
            self.y = SELECT_Y
        if select_count == 1:
            self.y = SELECT_Y + 80


class Box:
    def __init__(self, x, y, w, h, duration):  # ゲーム領域のコンストラクタ
        self.west, self.north = (x, y)
        self.east, self.south = (x + w, y + h)
        self.block = None  # 後で使うときはとりあえずNone
        self.ball = None
        self.duration = duration
        self.paddle1 = None
        self.paddle2 = None
        self.id = canvas.create_rectangle(x, y, x + w, y + h, fill="white", width=3)
        self.wall = None
        self.score = None
        self.select = None

    def create_block(self, x, y, w, h):  # ボール作成関数
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="black")  # 初期描写
        return Block(id, x, y, w, h)  # クラスを生成して返す

    def set_block(self, BLOCKS_X, BLOCKS_Y):  # ブロックの描写関数（いい感じの説明が思いつかなかった）
        random.shuffle(BLOCKS_X)
        random.shuffle(BLOCKS_Y)
        for i in range(len(BLOCKS_X)):  # 4回繰り返す
            self.block = self.create_block(BLOCKS_X[i], BLOCKS_Y[i], BLOCK_W, BLOCK_H)  # クラスの代入
            blocks.append(self.block)  # ブロックリストに追加

    def create_ball(self, x, y, d, vx, vy):  # ボール作成関数
        id = canvas.create_oval(x, y, x + d, y + d, fill="black")  # 初期描写
        return Ball(id, x, y, d, vx, vy)  # クラスを生成して返す

    def set_balls(self):  # ボールの描写関数（いい感じの説明が思いつかなかった）
        self.ball = self.create_ball(BALL_INITIAL_X,
                                     BALL_INITIAL_Y + BALL_DIAMETER,
                                     BALL_DIAMETER, BALL_X_SPEED, BALL_Y_SPEED)  # クラスの代入

    def create_paddle(self, x, y, w, h):  # パドル作成関数
        id = canvas.create_rectangle(x, y, x + w, y + h, fill="blue")  # 初期描写
        return Paddle(id, x, y, w, h)  # クラスを生成して返す

    def set_paddle(self):  # パドルの描写関数（いい感じの説明が思いつかなかった）
        self.paddle1 = self.create_paddle(
            self.west,
            self.south - PADDLE_HEIGHT * 3,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )  # クラスの代入
        self.paddle2 = self.create_paddle(
            self.east - PLUNGER_WIDTH - 70,
            self.south - PADDLE_HEIGHT * 3,
            PADDLE_WIDTH, PADDLE_HEIGHT
        )  # クラスの代入

    def create_wall(self, x1, y1, x2, y2):
        id = canvas.create_line(x1, y1, x2, y2, width=3)
        return Wall(id, x1, y1, x2, y2)

    def set_wall(self, i):
        if i == 0:  # 縦線
            x1 = self.east - PLUNGER_WIDTH
            y1 = self.north + PLUNGER_HEIGHT
            x2 = self.east - PLUNGER_WIDTH
            y2 = self.south
        elif i == 1:  # 右上
            x1 = self.east - PLUNGER_WIDTH
            y1 = self.north
            x2 = self.east
            y2 = self.north + 50
        elif i == 2:  # 左下
            x1 = self.west
            y1 = self.paddle1.y - 50
            x2 = self.west + 50
            y2 = self.paddle1.y
        elif i == 3:  # 右下
            x1 = self.east - PLUNGER_WIDTH - 50
            y1 = self.paddle1.y
            x2 = self.east - PLUNGER_WIDTH
            y2 = self.paddle1.y - 50
        self.wall = self.create_wall(x1, y1, x2, y2)
        walls.append(self.wall)

    def create_score(self, score):
        canvas.create_rectangle(SCORE_RECT_X, SCORE_RECT_Y, SCORE_RECT_X + SCORE_RECT_W, SCORE_RECT_Y + SCORE_RECT_H,
                                width=3, fill="lightgrey")  # 枠作成
        id = canvas.create_text(SCORE_X, SCORE_Y, text=f"score：{score}", font=("", 15, "bold"), anchor="w")  # 文字idに保存
        return Score(id)  # id を返す

    def set_score(self):
        global point
        point = self.create_score(score)

    def check_box(self):  # 壁の判定関数
        if self.ball.y <= self.north:  # もし上壁を越えたら
            self.ball.vy = - self.ball.vy  # 反射させる
            self.ball.y = self.north
        if self.ball.x <= self.west or self.ball.x + self.ball.d >= self.east:
            self.ball.vx = - self.ball.vx
        if self.ball.y + self.ball.d >= self.south - 30 and self.ball.x >= self.east - PLUNGER_WIDTH:
            self.ball.vy = BALL_Y_SPEED

    def check_paddle(self, paddle):  # パドルの判定関数
        if self.ball.x + self.ball.d >= paddle.x \
                and self.ball.x <= paddle.x + paddle.w \
                and self.ball.y + self.ball.d >= paddle.y:  # もしパドルに当たったら
            self.ball.vy = - self.ball.vy * REACTION  # 反射させる
            self.ball.y = paddle.y - self.ball.d  # ボールをパドルの上にする

    def check_block(self):  # ブロックの判定関数
        global score
        for block in blocks:  # それぞれのブロックの判定
            if self.ball.y + self.ball.d >= block.y and self.ball.y <= block.y + block.h \
                    and self.ball.x + self.ball.d >= block.x and self.ball.x <= block.x + block.w:  # もしブロックに当たったら
                self.ball.vy = - self.ball.vy  # 反射させる
                canvas.delete(block.id)  # ブロックのidを削除
                blocks.remove(block)  # リストから削除
                score += 10
                s = Score(self.score)
                s.redraw()
        if len(blocks) == 0:
            self.set_block(BLOCKS_X, BLOCKS_Y)  # ブロックの初期描写

    def check_wall(self):
        count = 0  # インデックス用
        for wall in walls:
            if count == 0:
                if (wall.x1 - 1 >= self.ball.x >= wall.x1 - 5) and self.ball.y >= wall.y1:
                    self.ball.vx = - self.ball.vx
            elif count == 1:
                if self.ball.x >= self.east - PLUNGER_WIDTH and \
                        self.ball.y <= (self.ball.x - self.east) + self.north + 50:
                    self.ball.vy = -self.ball.vy  # y方向に跳ね返る
                    self.ball.y = (self.ball.x - self.east) + self.north + 50
            elif count == 2:
                if self.ball.x <= self.west + 50 and \
                        self.ball.y >= (self.ball.x - (self.west + 50)) + self.paddle1.y:
                    self.ball.vy = -self.ball.vy  # y 方向に跳ね返る
                    self.ball.y = (self.ball.x - (self.west + 50)) + self.paddle1.y - self.ball.d  # 線上にする
            elif count == 3:
                if self.east - PLUNGER_WIDTH - 50 <= self.ball.x <= self.east - PLUNGER_WIDTH and \
                        self.ball.y >= - (self.ball.x - (self.east - PLUNGER_WIDTH - 50)) + self.paddle1.y:
                    self.ball.vy = -self.ball.vy  # y 方向に跳ね返る
                    self.ball.y = - (
                            self.ball.x - (self.east - PLUNGER_WIDTH - 50)) + self.paddle1.y - self.ball.d  # 線上にする
            count += 1

    def start(self):  # スタート画面作成関数
        global start_rect, start_text
        start_rect = canvas.create_rectangle(START_RECT_X, START_RECT_Y, START_RECT_X + START_RECT_W,
                                             START_RECT_Y + START_RECT_H, fill="lightgrey", width=2)  # 枠作成
        start_text = canvas.create_text(TEXT_X, TEXT_Y, text="START \n (space)",
                                        font=("", 50, "bold"), anchor="w")  # 文字作成

    def create_select(self, x, y, w, h):  # 選択画面作成関数
        global select_rect, select_text1, select_text2
        select_rect = canvas.create_rectangle(START_RECT_X, START_RECT_Y, START_RECT_X + START_RECT_W,
                                              START_RECT_Y + START_RECT_H, fill="lightgrey", width=2)  # 外枠
        id = canvas.create_rectangle(x, y, x + w, y + h, width=5)  # 選択枠
        select_text1 = canvas.create_text(TEXT_X - 10, TEXT_Y - 30, text="最初から",
                                          font=("", 50, "bold"), anchor="w")  # 最初から
        select_text2 = canvas.create_text(TEXT_X - 10, TEXT_Y + 50, text="続きから",
                                          font=("", 50, "bold"), anchor="w")  # 続きから
        return Select(id, x, y, w, h)  # 選択枠を返す

    def set_select(self):
        self.select = self.create_select(SELECT_X, SELECT_Y, SELECT_W, SELECT_H)

    def read_score(self):
        global score
        count = 0
        if select_count == 1 and count == 0:  # 下選んで一回目なら
            with open(r"db.txt") as file:  # ファイルを読み込む
                score = int(file.readline())  # score に代入
                s = Score(self.score)
                s.redraw()
            count = 1  # 1にする

    def finish(self):
        if select_count == 1:
            with open(r"db.txt", mode="w") as file:  # ファイルに書き込む
                file.write(str(score))
        canvas.create_text(TEXT_X - 120, TEXT_Y, text="～GAME OVER～", font=("", 45, "bold"), fill="red", anchor="w")

    def left_paddle(self, event):  # 左のイベント関数
        self.paddle1.x = self.west + 50  # 左に移動

    def right_paddle(self, event):  # 右のイベント関数
        self.paddle2.x = self.east - PLUNGER_WIDTH - 120  # 右に移動

    def back_left_paddle(self, event):  # ストップ関数
        self.paddle1.x = self.west  # ストップ

    def back_right_paddle(self, event):  # ストップ関数
        self.paddle2.x = self.east - PLUNGER_WIDTH - 70  # ストップ

    def play_start(self, event):
        global start_count
        if start_count == 0:  # １回目
            canvas.delete(start_rect, start_text)  # 最初の画面を削除
        elif start_count == 1:  # ２回目
            canvas.delete(select_rect, self.select.id, select_text1, select_text2)  # 選択画面を削除
            self.read_score()
        start_count += 1

    def select_up(self, event):  # 上押したら
        global select_count
        select_count = 0

    def select_down(self, event):  # 下押したら
        global select_count
        select_count = 1

    def set(self):
        self.set_score()
        self.set_balls()  # ボールの初期描写
        self.set_paddle()  # パドルの初期描写
        self.set_block(BLOCKS_X, BLOCKS_Y)  # ブロックの初期描写
        for i in range(4):
            self.set_wall(i)
        self.set_select()
        self.start()

    def check(self):
        self.check_box()  # 壁の判定
        for paddle in [self.paddle1, self.paddle2]:
            self.check_paddle(paddle)  # パドルの判定
        self.check_block()  # ブロックの判定
        self.check_wall()

        canvas.bind_all('<KeyPress-Left>', self.left_paddle)  # もし左を押したら、パドルを左に
        canvas.bind_all('<KeyPress-Right>', self.right_paddle)  # もし右を押したら、パドルを右に
        canvas.bind_all('<KeyRelease-Left>', self.back_left_paddle)  # もし左を放したら、ストップ
        canvas.bind_all('<KeyRelease-Right>', self.back_right_paddle)  # もし右を押したら、ストップ
        canvas.bind_all("<KeyPress-space>", self.play_start)
        canvas.bind_all("<KeyPress-Up>", self.select_up)
        canvas.bind_all("<KeyPress-Down>", self.select_down)

    def animate(self):
        objects = [self.select, self.paddle1, self.paddle2, self.ball]  # ボール、パドルクラスのリスト（ポリモーフィズム用）

        while True:
            for obj in objects:  # クラスのリストをforで回す（ポリモーフィズム用）
                obj.move()  # パドルかボールの移動
                if start_count < 3 and objects[3]:
                    break
            self.check()
            for obj in objects:  # クラスのリストをforで回す（ポリモーフィズム用）
                obj.redraw()  # パドルかボールの再描写

            if self.ball.y + self.ball.d >= self.south:  # もし下に当たったら  ←-- 関数にするとbreakが使えないから、これは直接！
                self.finish()
                break  # 終了
            time.sleep(self.duration)
            tk.update()


# main
tk = Tk()
tk.title("Game")  # 左上のタイトルを書ける

canvas = Canvas(tk, width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT, bd=0)
canvas.pack()

box = Box(BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT, duration=DURATION)  # ボールクラス生成
box.set()
box.animate()  # アニメーション(実行)
tk.mainloop()
