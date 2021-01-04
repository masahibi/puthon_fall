# 20K1026 日比野将己
#  第10回-課題[2]
# --------------------------
# プログラム名: ex10-maze-player.py

from dataclasses import dataclass, field
from tkinter import *
from maze import Maze  # from ファイル名 import クラス名（mazeモジュールのMazeクラスをimport）

x = 50  # 正方形の情報
y = 50
W = 50
H = 50

I = x * 2 + 10    # プレイヤーの座標
J = y + 10


@dataclass
class MazeGame:
    maze: Maze = field(init=False, default=None)  # init=False・・・コンストラクタでは初期化しない
    # 属性mazeにはMazeオフジェクトを割り当てる           # default=None・・・省略値はNone(self_floormapで初期化)
    player: tuple = field(init=False, default=None)    # tuple・・・組（離散とかのやつ）

    def print_floormap(self):  # マップ出力メソッド
        for i in self.maze.floormap:  # データリストから取り出す
            line = ""  # １行用の変数用
            for j in i:  # 入れ子から取り出す
                if j == 1:  # 要素が１なら
                    mark = "■"  # 四角に■
                else:  # 0なら
                    mark = "　"  # 空白に
                line += mark  # markを結合
            print(line)  # １行出力

    def draw_floormap(self):  # マップ描写メソッド
        global x, y
        x0 = x  # 初期ｘ座標保存
        for i in self.maze.floormap:  # データリストから取り出す
            for j in i:  # 入れ子から取り出す
                if j == 1:  # 要素が１なら
                    canvas.create_rectangle(x, y, x + W, y + H, fill="blue")  # 青い四角を描写
                x += W  # x座標を幅分右へ
            x = x0  # x座標を一番左へ
            y += H  # y座標を高さ分下へ

    def set_player(self, i, j):    # プレイヤーの初期位置メソッド
        self.player = (i, j)    # プレイヤーの座標を i, j にする

    def draw_player(self):    # プレイヤーの描写メソッド
        print(self.player)    # プレイヤーの座標確認用
        d = 30    # プレイヤーの大きさ
        canvas.create_oval(self.player[0], self.player[1], self.player[0] + d, self.player[1] + d, fill="red")
        # プレイヤーの丸を描写

    def redraw(self):    # 再描写メソッド
        self.print_floormap()  # map出力メソッド
        self.draw_floormap()  # map描写メソッド
        self.draw_player()    # プレイヤー描写メソッド

    def start(self):    # メイン処理メソッド
        self.maze = Maze()  # Mazeクラスのインスタンス化
        data = [  # 初期マップデータ
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1]
        ]
        self.maze.set_floormap(3, 4, data)  # 初期設定メソッド
        self.maze.from_file(r"maze_small.txt")  # ファイルからデータ読み込みメソッド
        self.set_player(I, J)    # プレイヤーの初期位置メソッド
        self.redraw()    # 再描写メソッド


tk = Tk()
canvas = Canvas(tk, width=600, height=700)
canvas.pack()

game = MazeGame()  # インスタンス化
game.start()    # メイン処理メソッド

tk.mainloop()
