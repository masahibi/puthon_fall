# Python によるプログラミング：第 3 章　
# 例題プログラム 2. フラップ
# --------------------------
# プログラム名: 03-flap.py

from tkinter import *
from dataclasses import dataclass
import random
import math
import time

# 初期データ
DURATION = 0.005   # sleep時間=描画の間隔
DIAMETER = 10      # ボールの直径
STEPS = 9000       # コマ数
LEFT = 100         # 左端
RIGHT = 500        # 右端
TOP = 100          # 上側の落ち始める位置
BOTTOM = 700       # 下側の地面位置
WALL_THICKNESS = 1 # 壁の厚さ
GRAVITY = 0.2      # 重力
REFLECTION = 1.0   # 反射係数
FLAP_SPEED = 5     # フラップの速さ
VY_MAX = 25        # プランジャーの最高速度

# 壁の種類
VIRTICAL_WALL = 1
HORIZONTAL_WALL = 2
SLANT_WALL = 3

# キーの状態
KEY_RELEASED = 0
KEY_PRESSED = 1

@dataclass
class Ball:
    id: int
    x: float
    y: float
    d: float
    vx: float
    vy: float
    bcolor: str


@dataclass
class Wall:
    x1: float
    y1: float
    x2: float
    y2: float
    reflection: float
    thickness: int
    color: str

    def draw(self):
        self.id = canvas.create_line(self.x1, self.y1, self.x2, self.y2,
                                     width=self.thickness, fill=self.color)

    # 壁の種類と、係数を計算する
    def initialize(self):
        if self.x1 == self.x2:
            self.wall_type = VIRTICAL_WALL
            self.slope = None   # 無限大なので、利用しない
            self.offset = None  # トラップ
            self.vector = math.pi / 2.0
        elif self.y1 == self.y2:
            self.wall_type = HORIZONTAL_WALL
            self.slope = 0
            self.offset = self.y1
            self.vector = 0.0
        else:
            self.wall_type = SLANT_WALL
            self.set_slope(self.x2, self.y2)
            # self.slope = float(self.y1-self.y2)/float(self.x1-self.x2)
            # self.offset = self.y1 - self.slope * self.x1
            # self.vector = math.atan2(-float(self.y1-self.y2), float(self.x1-self.x2))

    # 一次関数の傾き
    def set_slope(self, x3, y3):
        self.slope = float(self.y1 - y3)/float(self.x1 - x3)
        self.offset = self.y1 - self.slope * self.x1
        self.vector = math.atan2(-float(self.y1 - y3), float(self.x1 - x3))

    # 反射の一般化
    # このメソッドで、縦、横、斜め全ての壁に対応する。
    def bound(self, ball):
        new_ball_x = ball.x + ball.vx  # 反射せずに移動後の x 座標
        new_ball_y = ball.y + ball.vy  # 移動した後 y座標
        # 垂直の壁だけは、別扱い: arctanの定義域
        if self.wall_type == VIRTICAL_WALL:
            # 壁をまたぐ移動があると、差分の符号が負になる。
            diff = (self.x1 - ball.x) * (self.x1 - new_ball_x)
            if (diff <= 0 and \
                ((self.y1 <= new_ball_y <= self.y2) or \
                 (self.y2 <= new_ball_y <= self.y1))) or \
               ((new_ball_x < self.x1 and self.x1 - new_ball_x <= ball.d/2) or \
                (new_ball_x > self.x1 and new_ball_x - self.x1 <= ball.d/2)):
                # 反射が起きる。
                ball.vx = -self.reflection * ball.vx
                if self.x1 > ball.x:  # 左からの衝突
                    ball.x = self.x1 - ball.d/2    # 壁に貼り付ける
                else:
                    ball.x = self.x1 + ball.d/2
                return True
            else:
                return False
        elif self.wall_type == HORIZONTAL_WALL:
            # 壁をまたぐ移動があると、差分の符号が負になる。
            diff = (self.y1 - ball.y) * (self.y1 - new_ball_y)
            if (diff <= 0 and \
                ((self.x1 <= new_ball_x <= self.x2) or \
                 (self.x2 <= new_ball_x <= self.x1))):
                # 反射が起きる。
                ball.vy = -self.reflection * ball.vy
                if self.y1 > ball.y:  # 上からの衝突
                    ball.y = self.y1 - ball.d/2    # 壁に貼り付ける
                else:
                    ball.y = self.y1 + ball.d/2
                return True
            else:
                return False
        else:
            old_y = self.slope * ball.x + self.offset  # 移動前のXに対する壁のY
            new_y = self.slope * new_ball_x + self.offset   # 移動後のXに対する壁のY
            diff = (old_y - ball.y) * (new_y - new_ball_y)
            if (diff <= ball.d * ball.d / 4 and \
                ((self.x1 <= new_ball_x <= self.x2) or \
                 (self.x2 <= new_ball_x <= self.x1))):
                # 反射が起きる
                # ball の vxが 0でない場合は、tan の定義域に注意
                if ball.vx == 0:
                    if -ball.vy >= 0:   # 真上に向かっている。
                        ball_vector = math.pi / 2
                    else:  # 真下に向かっている。 画面座標の下が+なのに注意
                        ball_vector = -math.pi / 2
                else:
                    ball_vector = math.atan2(-ball.vy, ball.vx)
                # 新しい反射角
                new_angle = 2 * self.vector - ball_vector
                # 分子と分母に同じようにreflectionがかかる
                norm = math.hypot(ball.vx, ball.vy)
                # 角度とベクトルから、新しい ball.vx と ball.vyを求める
                ball.vx = self.reflection * norm * math.cos(new_angle)
                ball.vy = -self.reflection * norm * math.sin(new_angle)
                return True
            else:
                return False


class Flap(Wall):
    def __init__(self, x1, y1, x2, y2, reflection, thickness, color, key):
        super().__init__(x1, y1, x2, y2, reflection, thickness, color)
        self.key = key

    def initialize(self):
        self.key_status = KEY_RELEASED
        super().initialize()
        # 三角関数で、xを展開する
        self.theta = math.atan((self.y2 - self.y1)/(self.x2 - self.x1))
        self.delta = -2 * self.theta / 10.
        self.flap_moving = 0
        self._job_move = None
        self.norm = (self.x2 - self.x1) / math.cos(self.theta)
        # self.y3 = 2 * self.y1 - self.y2
        canvas.bind_all(("<KeyPress-%c>" % self.key), self.check_up)
        # canvas.bind_all(("<KeyRelease-%c>" % self.key), self.check_down_2)

    def check_down_2(self, event):
        print(f"Key-{self.key}:Released")

    def check_up(self, event):
        if self.key_status == KEY_RELEASED:
            print(f"Key-{self.key}:Pressed")
            self.key_status = KEY_PRESSED
            self.up(event)
            self._job = tk.after(550, self.check_down)
        elif self.key_status == KEY_PRESSED:
            tk.after_cancel(self._job)
            self._job = tk.after(250, self.check_down)

    def check_down(self):
        print(f"Key-{self.key}:Released")
        if self.key_status == KEY_PRESSED:
            self.key_status = KEY_RELEASED
            self.down()
        else:
            pass

    def up(self, event):
        self._job_move = tk.after(FLAP_SPEED, self.move)
        self.flap_moving = 1
        tk.update()

    def move(self):
        theta = self.theta + self.flap_moving * self.delta
        x3 = self.norm * math.cos(theta) + self.x1
        y3 = self.norm * math.sin(theta) + self.y1
        canvas.coords(self.id, self.x1, self.y1, x3, y3)
        self.set_slope(x3, y3)
        tk.update()
        self.flap_moving += 1
        if self.flap_moving > 10:
            self.flap_moving = 0
            self._job_move = None
        else:
            self._job_move = tk.after(FLAP_SPEED, self.move)

    def down(self):
        if self._job_move:
            tk.after_cancel(self._job_move)
            self._job_move = None
        canvas.coords(self.id, self.x1, self.y1, self.x2, self.y2)
        self.set_slope(self.x2, self.y2)
        # canvas.itemconfigure(self.id, fill=self.color)
        tk.update()


class Plunger:
    def __init__(self, ball):
        self.ball = ball
        self.vy = 0
        self._job = None
        self.id = None
        canvas.bind_all("<KeyPress-space>", self.check_up)

    def check_up(self, event):
        self.up(event)
        if self._job:
            tk.after_cancel(self._job)
        self._job = tk.after(250, self.released)

    def up(self, event):
        # print("charged")
        self.vy += 2
        if self.vy >= VY_MAX:
            self.vy = VY_MAX
        if self.id:
            canvas.coords(self.id, RIGHT-25, BOTTOM - 4*self.vy -2,
                          RIGHT-5, BOTTOM-2)
        else:
            self.id = canvas.create_rectangle(RIGHT-25, BOTTOM - 4*self.vy -2,
                                              RIGHT-5, BOTTOM-2,
                                              outline="red", fill="red")
        tk.update()

    def released(self):
        global run
        # print("released")
        self.ball.vy = -self.vy
        self.ball.vx = 0
        self.ball.x = RIGHT - 35 + self.ball.d/2
        self.ball.y = BOTTOM - 4*self.vy - 5
        canvas.delete(self.id)
        self.id = None
        run = True


# ボールを初期位置に描画する。
def make_ball(x, y, d, vx, vy, bcolor):
    #　座標の0,0,0,0は、ダミーの値
    id = canvas.create_oval(0, 0, 0, 0,
                            fill=bcolor, outline=bcolor)
    return Ball(id, x, y, d, vx, vy, bcolor)

# ボールの動き
def move_ball(ball):
    if (ball.vy < 0) and (ball.vy + GRAVITY > 0):  # 向きが変わる
        ball.vy = 0   # 一旦止める
    else:
        ball.vy += GRAVITY
    ball.y += ball.vy
    ball.x += ball.vx

# ボールの再描画
def redraw_ball(ball):
    id = ball.id
    x = ball.x
    y = ball.y
    r = ball.d/2       # ボールの半径
    canvas.coords(id, x-r, y-r, x+r, y+r)

# プログラム本文
tk=Tk()
canvas = Canvas(tk, width=600, height=800, bd=0)
canvas.pack()
tk.update()

# ボールのデータ
vx = random.choice([-4. -3., -2., 2., 3., 4.])
ball = make_ball(200, TOP+DIAMETER+20, DIAMETER, vx, 0, "blue")

# 枠の描画
walls = [
    Wall(LEFT, TOP, LEFT, BOTTOM, 1.0, WALL_THICKNESS, "black"),
    Wall(LEFT, BOTTOM, RIGHT, BOTTOM, 1.0, WALL_THICKNESS, "black"),
    Wall(RIGHT, TOP, RIGHT, BOTTOM, 1.0, WALL_THICKNESS, "black"),
    Wall(LEFT, TOP, RIGHT, TOP, 1.0, WALL_THICKNESS, "black"),
    Wall(RIGHT-150, TOP, RIGHT, TOP+200, 1.0, 3, "blue"),
    Wall(RIGHT-40, 400, RIGHT-40, BOTTOM, 1.0, 2, "blue"),
    Wall(LEFT, 430, LEFT+120, 550, 0.7, 6, "orange"),
    Wall(RIGHT-160, 550, RIGHT-40, 430, 0.7, 6, "orange"),
    ]

flaps = [
    Flap(LEFT+120, 550, LEFT+160, 590, 1.1, 10, "green", 'z'),
    Flap(RIGHT-160, 550, RIGHT-200, 590, 1.1, 10, "green", '/')
    ]

plunger = Plunger(ball)

for wall in walls:
    wall.initialize()
    wall.draw()

for flap in flaps:
    flap.initialize()
    flap.draw()
    walls.append(flap)

# 開始メッセージ
msg_id = canvas.create_text((RIGHT+LEFT)/2, 200, text="SPACE to charge",
                   font=("FixedSys", 16), justify="center",
                   anchor=CENTER)
tk.update()

run = False
while not run:
    tk.update()           # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleepする。
canvas.delete(msg_id)
tk.update()

# 全体のプログラムのループ
for s in range(STEPS):
    for wall in walls:
        wall.bound(ball)
    move_ball(ball)
    redraw_ball(ball)     # 描画を反映させる。
    tk.update()           # 描画が画面に反映される。
    time.sleep(DURATION)  # 次に描画するまで、sleepする。
