# 20K1026 日比野将己
#  第12回-課題[1]
# --------------------------
# プログラム名: ex12-1-flowers.py

import pygame  # モジュールのインポート

RED = (255, 0, 0)  # (R,G,B)　赤
PURPLE = (128, 0, 128)  # 紫
WHITE = (255, 255, 255)  # 白
BRACK = (0, 0, 0)  # 黒

screen = pygame.display.set_mode((700, 400))  # ディスプレイの生成
screen.fill(WHITE)  # 背景色を白に
image = pygame.Surface((300, 300))  # 画像描写用の Surface（仮想画面）を生成
image.fill(BRACK)  # Surface の背景色を白に
draw = pygame.draw  # モジュールの定義（使いやすいように）


draw.circle(image, RED, (100, 50), 50)  # Surface の(50, 50)に赤い大きさ50の丸を描写  上
draw.circle(image, RED, (160, 110), 50)  # 右
draw.circle(image, RED, (100, 170), 50)  # 下
draw.circle(image, RED, (50, 110), 50)  # 左
draw.circle(image, PURPLE, (100, 110), 40)  # 中心


image.set_colorkey((0, 0, 0))  # Surface を透明に
screen.blit(image, (00, 25))  # ディスプレイの(100, 100)に Surface を転送
screen.blit(image, (200, 150))  # ディスプレイの(100, 100)に Surface を転送
screen.blit(image, (400, 25))  # ディスプレイの(100, 100)に Surface を転送
pygame.display.flip()  # 描写の反映（ここで表示される）
