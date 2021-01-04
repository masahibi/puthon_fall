# 20K1026 日比野将己
#  第12回-課題[3]
# --------------------------
# プログラム名: ex12-3-bouncing.py

import pygame  # モジュールのインポート

FPS = 60  # 毎秒のフレーム遅延
LOOP = True  # ループの判定
GRAVITY = 0.5  # 重力
d = 70  # ボールの大きさ
count = 0  # 当たり判定用

RED = (255, 0, 0)  # 黄色
WHITE = (255, 255, 255)  # 白


def draw_ball(screen, x, y, radius=10):  # ボールの描写関数
    pygame.draw.circle(screen, RED, (x, y), radius)  # ディスプレイに黄色で(x,y)に大きさ10の円を描写


screen = pygame.display.set_mode((700, 500))  # ディスプレイの生成
screen.fill(WHITE)  # 背景色を白に
image = pygame.Surface((100, 100))  # 画像描写用の Surface（仮想画面）を生成
background = pygame.image.load("hosei.jpg")  # 背景画像を読み込む
background = pygame.transform.scale(background, (600, 400))  # 背景画像を縮小（判定が分かりやすいようにディスプレイより小さくした）
ball = pygame.image.load("eco.jpg")  # ボール画像を読み込む
ball = pygame.transform.scale(ball, (d, d))  # ボールを縮小
ball = ball.convert()  # 画像を変換する
ball.set_colorkey(ball.get_at((0, 0)))  # 左上の(0,0)を背景色に指定
change_ball = pygame.transform.flip(ball, True, False)  # ボールを左右に反転
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
    if not (0 <= x <= 530):  # もしディスプレイの左右内じゃなかったら
        vx = -vx  # ボールを反射させる
        count += 1  # +1 する（偶奇で判定するため）
    if not (0 <= y + d <= 400):  # もしディスプレイの上下内じゃなかったら
        vy = -vy * 0.99  # ボールを反射させる
        y = 400 - d  # ボールの下を背景画像の下にする（入り込み防止）
    # draw_ball(screen, x, y)  # ボールの描写
    screen.blit(background, (0, 0))  # ディスプレイに背景画像を転送
    if count % 2 == 0:  # もし判定カウントが偶数（左に当たった）なら
        screen.blit(ball, (x, y))  # ディスプレイにボールを転送
    else:  # 奇数（右に当たった）なら
        screen.blit(change_ball, (x, y))  # ディスプレイに反転ボールを転送
    pygame.display.flip()  # 描写の反映
    screen.fill(WHITE)  # 塗りつぶし

pygame.quit()  # 画面を閉じる
