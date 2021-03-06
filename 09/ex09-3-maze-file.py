# 20K1026 日比野将己
#  第9回-課題[3]
# --------------------------
# プログラム名: ex09-3-maze-file.py

from dataclasses import dataclass, field


@dataclass
class MazeGame:
    height: int = field(init=False, default=None)    # init=False・・・コンストラクタでは初期化しない
    width: int = field(init=False, default=None)     # default=None・・・省略値はNone(self_floormapで初期化)
    floormap: list = field(init=False, default=None)

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


game = MazeGame()
game.from_file(r"maze.txt")
print(game)
