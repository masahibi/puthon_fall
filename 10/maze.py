# 20K1026 日比野将己
#  第10回-課題[1]
# --------------------------
# プログラム名: maze.py

from dataclasses import dataclass, field

# X = 50  # 正方形の情報
# Y = 50
# W = 50
# H = 50


@dataclass
class Maze:
    height: int = field(init=False, default=None)  # init=False・・・コンストラクタでは初期化しない
    width: int = field(init=False, default=None)  # default=None・・・省略値はNone(self_floormapで初期化)
    floormap: list = field(init=False, default=None)

    def set_floormap(self, height, width, floormap):  # 初期化メソッド
        self.height = height
        self.width = width
        self.floormap = floormap

    def from_file(self, filename):  # ファイル読み込みメソッド
        self.floormap = []
        with open(filename) as file:  # ファイル読み込み
            first_line = file.readline().rstrip("\n")  # １行読み込み（改行削除）
            w_h = first_line.split(",")  # , で分割リスト
            self.height = w_h[0]
            self.width = w_h[1]
            for line in file:  # ファイルから１行ずつ取り出す
                lines = []  # １行用リスト
                for x in line.rstrip("\n"):  # 改行抜きの行で取り出す
                    lines.append(int(x))  # リストに追加（読み込んできたものは文字列なのでint化）
                self.floormap.append(lines)  # １行リストに追加


# game = Maze()  # インスタンス化
# maze = [  # マップデータ
#     [1, 0, 1, 1],
#     [1, 0, 0, 1],
#     [1, 1, 0, 1]
# ]
# game.set_floormap(3, 4, maze)  # 初期設定メソッド
# game.from_file(r"maze_small.txt")

