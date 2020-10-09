from tkinter import *
from dataclasses import dataclass

WALL_THICKNESS = 10
STEPS = 100


@dataclass
class Wall:
    x1: int
    y1: int
    x2: int
    y2: int
    reflection: float
    thickness: int
    color: str


def draw_wall(wall):
    wall.id = canvas.create_line(wall.x1, wall.y1,
                                 wall.x2, wall.y2,
                                 width=wall.thickness,
                                 fill=wall.color)


def bound(wall, ball):
    print(1)
    # ここに、壁とボールの衝突処理を記述する。
    # 教科書の例題、練習問題の解答例プログラムなどを参照のこと


# 枠の描画
# 壁を、イテレータで反復処理させます。
walls = [
    Wall(LEFT, TOP, LEFT, BOTTOM, 1.0,
         WALL_THICKNESS, "black"),
    Wall(LEFT, BOTTOM, RIGHT, BOTTOM, 1.02,
         WALL_THICKNESS, "black"),
    Wall(RIGHT, TOP, RIGHT, BOTTOM, 1.0,
         WALL_THICKNESS, "black"),
    Wall(LEFT, TOP, RIGHT, TOP, 1.0,
         WALL_THICKNESS, "black"),
    Wall(300, 300, 400, 500, 1.01, 6, "orange")
]

tk = Tk()
canvas = Canvas(tk, width=800, height=600)
canvas.pack()
canvas.update()

for wall in walls:
    draw_wall(wall)
# 全体のプログラムのループ
for s in range(STEPS):
    for wall in walls:
        bound(wall, 1)

tk.mainloop()
