# 20K1026 日比野将己
#  第9回-課題[4]
# --------------------------
# プログラム名: ex09-4-maze-print.py

from dataclasses import dataclass, field


@dataclass
class MazeGame:
    height: int = field(init=False, default=None)    # init=False・・・コンストラクタでは初期化しない
    width: int = field(init=False, default=None)     # default=None・・・省略値はNone(self_floormapで初期化)
    floormap: list = field(init=False, default=None)

    def set_floormap(self, height, width, floormap):    # 初期化メソッド
        self.height = height
        self.width = width
        self.floormap = floormap

    def print_floormap(self):    # マップ出力メソッド
        for x in self.floormap:    # データリストから取り出す
            line = ""    # １行用の変数用
            for y in x:    # 入れ子から取り出す
                if y == 1:    # 要素が１なら
                    mark = "■"    # 四角に
                else:    # 0なら
                    mark = "　"    # 空白に
                line += mark    # markを結合
            print(line)    # １行出力


game = MazeGame()    # インスタンス化
maze = [    # マップデータ
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1]
]
game.set_floormap(3, 4, maze)    # 初期設定メソッド
game.print_floormap()    # マップ出力メソッド
