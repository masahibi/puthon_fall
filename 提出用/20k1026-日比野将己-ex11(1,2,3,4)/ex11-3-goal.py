# 20K1026 日比野将己
#  第11回-課題[3]
# --------------------------
# プログラム名: ex11-3-goal.py

from dataclasses import dataclass, field
from tkinter import *
from maze import Maze  # from ファイル名 import クラス名（mazeモジュールのMazeクラスをimport）
import random
import time

x = 50  # 正方形の情報
y = 50
W = 50
H = 50

player_X = x  # プレイヤーの初期値（左上の四角の場所）
player_Y = y


@dataclass
class MazeGame:
    maze: Maze = field(init=False, default=None)  # init=False・・・コンストラクタでは初期化しない
    # 属性mazeにはMazeオフジェクトを割り当てる           # default=None・・・省略値はNone(self_floormapで初期化)
    player: tuple = field(init=False, default=None)  # tuple・・・組（離散とかのやつ）

    def __init__(self):
        self.location = None
        self.goal = False

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
        y0 = y  # 初期y座標保存
        for i in range(int(self.maze.height)):  # 〇行目
            for j in range(int(self.maze.width)):  # 〇列目
                if self.maze.floormap[i][j] == 1:  # 壁なら
                    canvas.create_rectangle(x, y, x + W, y + H, fill="blue")  # 青い四角を描写
                elif self.maze.floormap[i][j] == 2:  # スタートなら
                    canvas.create_rectangle(x, y, x + W, y + H, fill="lightblue")  # 水色の四角を描写
                elif self.maze.floormap[i][j] == 3:  # ゴールなら
                    canvas.create_rectangle(x, y, x + W, y + H, fill="lightgreen")  # 黄緑の四角を描写
                elif self.maze.floormap[i][j] == 4:  # 通過点なら
                    canvas.create_rectangle(x, y, x + W, y + H, fill="yellow")  # 黄色の四角を描写
                elif self.maze.floormap[i][j] == 5:  # 自分なら
                    self.location = [i, j]  # 行列のインデックスを代入
                    print(self.location)  # インデックスリスト
                    self.set_player(x + 10, y + 10)  # 位置の再設定（組は値を変えれないため、再度setし直す必要がある）
                x += W  # x座標を幅分右へ
            x = x0  # x座標を一番左へ
            y += H  # y座標を高さ分下へ
        y = y0  # x座標を一番左へ

    def set_player(self, i, j):  # プレイヤーの初期位置メソッド
        self.player = (i, j)  # プレイヤーの座標を i, j にする

    def draw_player(self):  # プレイヤーの描写メソッド
        print(self.player)  # 組の座標
        d = 30  # プレイヤーの大きさ
        canvas.create_oval(self.player[0], self.player[1], self.player[0] + d, self.player[1] + d, fill="red")
        # プレイヤーの〇を表示

    def redraw(self):
        canvas.delete("all")  # 描写すべて削除
        self.print_floormap()  # map出力メソッド
        self.draw_floormap()  # map描写メソッド
        self.draw_player()  # プレイヤー描写メソッド
        if self.goal:  # もしgoalがTrueなら
            canvas.create_text(300, 300, text="Win！", font=("", 50, "bold"), fill="red")  # Wn!と描写

    def random_move(self):  # ランダムで移動するメソッド
        x = random.choice([-1, 0, 1])  # -1,0,1でランダム
        y = 0
        if x == 0:  # もし横に動かなかったら
            y = random.choice([-1, 1])  # -1,1でランダム
        if self.maze.floormap[self.location[0] + y][self.location[1] + x] == 1:  # 壁なら
            self.random_move()  # もう一回実行
        elif self.maze.floormap[self.location[0] + y][self.location[1] + x] == 3:  # もし移動先がゴールなら
            self.goal = True  # goalをTrueに
        elif self.maze.floormap[self.location[0] + y][self.location[1] + x] == 0:  # 移動先が通路なら
            self.maze.floormap[self.location[0] + y][self.location[1] + x] = 5  # 移動先を自分に
            self.maze.floormap[self.location[0]][self.location[1]] = 0  # 今の場所を通過点に
        self.redraw()  # 再描写

    def start(self):  # メイン処理メソッド
        self.maze = Maze()  # Mazeクラスのインスタンス化
        data = [  # 初期マップデータ
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 1, 0, 1]
        ]
        self.maze.set_floormap(3, 4, data)  # 初期設定メソッド
        self.maze.from_file(r"ex11-2-move.txt")  # ファイルからデータ読み込みメソッド
        self.redraw()  # 再描写メソッド

        while True:
            self.random_move()  # ランダム移動メソッド
            tk.update()  # 再描写
            time.sleep(0.1)  # 0.5秒停止
            if self.goal:  # もしgoalがTrueなら
                break  # ループ抜ける


tk = Tk()
canvas = Canvas(tk, width=600, height=700)
canvas.pack()

game = MazeGame()  # インスタンス化
game.start()  # メイン処理メソッド

tk.mainloop()
