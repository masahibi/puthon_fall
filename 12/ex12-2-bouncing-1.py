# 20K1026 日比野将己
#  第12回-課題[2-1]
# --------------------------
# プログラム名: ex12-2-bouncing-1.py

import pygame  # モジュールのインポート

FPS = 60  # 毎秒のフレーム数
LOOP = True  # ループの判定
GRAVITY = 0.5  # 重力

RED = (255, 0, 0)  # 黄色
WHITE = (255, 255, 255)  # 白


def draw_ball(screen, x, y, radius=10):  # ボールの描写関数
    pygame.draw.circle(screen, RED, (x, y), radius)  # ディスプレイに黄色で(x,y)に大きさ10の円を描写


screen = pygame.display.set_mode((600, 400))  # ディスプレイの生成
screen.fill(WHITE)  # 背景色を白に
clock = pygame.time.Clock()  # 時計オブジェクト（こいつで FPS の遅延をかける）

x, y = (100, 100)  # ボールの初期位置
vx, vy = (5, 10)  # ボールの速度ｘ,y

while LOOP:  # 描写のループ
    for event in pygame.event.get():  # イベントが起こったときに来る
        if event.type == pygame.QUIT:  # もし閉じるボタンが押されたら
            LOOP = False  # ループを終わる
    clock.tick(FPS)  # 毎秒の呼び出し回数（フレームレート）
    x += vx  # ボールのｘ座標移動
    vy += GRAVITY  # 重力付加
    y += vy  # ボールのｙ座標移動
    if not (0 <= x <= 600):  # もしディスプレイの左右内じゃなかったら
        vx = -vx  # ボールを反射させる
    if not (0 <= y <= 400):  # もしディスプレイの上下内じゃなかったら（なぜかｙはこれ以外の判定は入り込む）
        vy = -vy  # ボールを反射させる
    draw_ball(screen, x, y)  # ボールの描写
    pygame.display.flip()  # 描写の反映
    screen.fill(WHITE)  # 塗りつぶし

pygame.quit()  # 画面を閉じる
