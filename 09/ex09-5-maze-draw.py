# 20K1026 日比野将己
#  第9回-課題[5]
# --------------------------
# プログラム名: ex09-5-maze-draw.py

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

    def set_floormap(self, height, width, floormap):    # 初期化メソッド
        self.height = height
        self.width = width
        self.floormap = floormap

    def from_file(self, filename):    # ファイル読み込みメソッド
        self.floormap = []
        with open(filename) as file:    # ファイル読み込み
            first_line = file.readline().rstrip("\n")    # １行読み込み（改行削除）
            w_h = first_line.split(",")    # , で分割リスト
            self.height = w_h[0]
            self.width = w_h[1]
            for line in file:    # ファイルから１行ずつ取り出す
                lines = []    # １行用リスト
                for x in line.rstrip("\n"):    # 改行抜きの行で取り出す
                    lines.append(int(x))    # リストに追加（読み込んできたものは文字列なのでint化）
                self.floormap.append(lines)    # １行リストに追加

    def print_floormap(self):  # マップ出力メソッド
        for x in self.floormap:  # データリストから取り出す
            line = ""  # １行用の変数用
            for y in x:  # 入れ子から取り出す
                if y == 1:  # 要素が１なら
                    mark = "■"  # 四角に■
                else:  # 0なら
                    mark = "　"  # 空白に
                line += mark  # markを結合
            print(line)  # １行出力

    def draw_floormap(self, x, y, w, h):    # マップ描写メソッド
        x0 = x    # 初期ｘ座標保存
        for i in self.floormap:    # データリストから取り出す
            for j in i:    # 入れ子から取り出す
                if j == 1:    # 要素が１なら
                    canvas.create_rectangle(x, y, x + w, y + h, fill="blue")    # 青い四角を描写
                x += w    # x座標を幅分右へ
            x = x0    # x座標を一番左へ
            y += h    # y座標を高さ分下へ


tk = Tk()
canvas = Canvas(tk, width=600, height=700)
canvas.pack()

game = MazeGame()    # インスタンス化
maze = [    # マップデータ
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1]
]
game.set_floormap(3, 4, maze)    # 初期設定メソッド
game.from_file(r"maze_small.txt")
game.print_floormap()    # マップ出力メソッド
game.draw_floormap(X, Y, W, H)    # マップ描写メソッド

tk.mainloop()
