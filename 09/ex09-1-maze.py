# 20K1026 日比野将己
#  第9回-課題[1]
# --------------------------
# プログラム名: ex09-1-maze.py

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


game = MazeGame()    # インスタンス化
maze = [    # マップデータ
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1]
]
game.set_floormap(3, 4, maze)    # 初期設定メソッド
print(game.floormap)
