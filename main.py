from tkinter import*
from dataclasses import dataclass
import time

#描画の間隔
DURATION=0.01
#バウンドの回数をここで調整
STEP=500
X=100
Y=100
D=50
#自由落下を見たいので、x軸方向の変化は0
vx=2
vy=2

@dataclass
class Ball:
    id:int
    x:int
    y:int
    d:int
    vx:int
    vy:int
    c:str

@dataclass
class Ground:
    x1:int
    y1:int
    width:int
    height:int

#地面と落とす位置を描画する。
def make_grounds(ox,oy,width,height):
    canvas.create_line(ox,oy,oy,oy)
    canvas.create_line(ox,height,ox+width,height)

#四角いボールを初期位置に
def make_ball(x,y,d,vx,vy,c="black"):
    id=canvas.create_rectangle(x,y,x+d,y+d,fill=c,outline=c)
    return Ball(id,x,y,d,vx,vy,c)

#ボールの移動に関する変化、x,yそれぞれを変化させる。4行目で重力を表現
def move_ball(ball):
    ball.x=ball.x+ball.vx
    ball.y=ball.y+ball.vy
    ball.vy=ball.vy+0.1



#ボールを再描画する。
def redraw_ball(ball):
    d=ball.d
    canvas.coords(ball.id,ball.x,ball.y,ball.x+d,ball.y+d)

tk=Tk()
canvas=Canvas(tk,width=600,height=800,bd=0)
canvas.pack()
tk.update()

#地面と落とす位置の座標を入力
ground=Ground(0,100,600,700)



make_grounds(
    ground.x1,
    ground.y1,
    ground.width,
    ground.height
    )

ball=make_ball(X,Y,D,vx,vy)

c=0
while True:
    c=c+1
    print(c)
    move_ball(ball)
    #Y座標が、地面と落とす位置を超えるならYの移動方向を反転させる
    if (ball.y<=ground.y1 or ball.y+ball.d>=ground.height):
        ball.vy=-ball.vy*0.9
    if c==2300:
        break
    redraw_ball(ball)
    tk.update()
    time.sleep(DURATION)
