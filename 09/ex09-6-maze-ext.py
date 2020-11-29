# 20K1026 日比野将己
#  第9回-課題[6]
# --------------------------
# プログラム名: ex09-6-maze-ext.py

from dataclasses import dataclass, field
from tkinter import *

X = 50    # 正方形の情報
Y = 50
W = 50
H = 50


@dataclass
class MazeGame:
    height: int = field(init=False, default=None)    # init=False・・・コンストラクタでは初期化しない
    width: int = field(init=False, default=None)     # default=None・・・省略値はNone(self_floormapで初期化)
    floormap: list = field(init=False, default=None)

    def set_floormap(self, height, width, floormap):     # 初期化メソッド
        self.height = height
        self.width = width
        self.floormap = floormap

    def print_floormap(self):  # マップ出力メソッド
        for x in self.floormap:  # データリストから取り出す
            line = ""  # １行用の変数用
            for y in x:  # 入れ子から取り出す
                if y == 1:  # 要素が１なら
                    mark = "■"  # 四角に
                else:  # 0なら
                    mark = "　"  # 空白に
                line += mark  # markを結合
            print(line)  # １行出力

    def draw_floormap(self, x, y, w, h):    # マップ描写メソッド
        x0 = x    # 初期ｘ座標保存
        count = 0    # 行数用
        for i in self.floormap:    # データリストから取り出す
            for j in i:    # 入れ子から取り出す
                if j == 1:    # 要素が１なら
                    canvas.create_rectangle(x, y, x + w, y + h, fill="blue")    # 青い四角を描写
                if count == 0 and j == 0:    # １行目で要素が0なら
                    canvas.create_text(x + w / 2, y + h / 2, text="S")    # Sと表示
                if count == self.height - 1 and j == 0:    # 最後の行で要素が0なら
                    canvas.create_text(x + w / 2, y + h / 2, text="G")    # Gと表示
                x += w    # x座標を幅分右へ
            x = x0    # x座標を一番左へ
            y += h    # y座標を高さ分下へ
            count += 1    # 行が変わるため＋１


tk = Tk()
canvas = Canvas(tk, width=400, height=600)
canvas.pack()

game = MazeGame()    # インスタンス化
maze = [    # マップデータ
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1]
]
game.set_floormap(3, 4, maze)    # 初期設定メソッド
game.print_floormap()    # マップ出力メソッド
game.draw_floormap(X, Y, W, H)    # マップ描写メソッド

tk.mainloop()
