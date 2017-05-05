# coding:utf-8
"""
map[X][Y]


player.moveUpdate()

map.setMoving(p_x_old,p_y_old,p_x_new,p_y_new)
stage.draw(map)

"""
from variable import *
# ワールド座標からプレイヤーを中心に表示する座標を切り出す
def cutWorldMapToDisplay(wMap,pX,pY,dispX,dispY):

    sX=pX-dispX/2
    eX=pX+dispX/2 #マップが正方形なのが前提
    if sX<0:
        sX=0
        eX=dispX
    elif eX>=len(wMap):
        sX = len(wMap)-dispX
        eX = len(wMap)

    sY=pY-dispY/2
    eY=pY+dispY/2 #マップが正方形なのが前提
    if sY<0:
        sY=0
        eY=dispY
    elif eY>=len(wMap):
        sY = len(wMap)-dispY
        eY = len(wMap)

    def cutOneLine(i,start,end):
        return wMap[int(sY+i)][int(start):int(end)]
    res=[]
    for y in range(int(dispY)):
        res.append(cutOneLine(y,sX,eX))
    print(res)
    return res


def is_movalbe(y,x):

    """
    0:行ける
    1:敵
    2:行けない 
    """
    x,y=int(x),int(y)
    if (x< 0) or (x >= 256) or (y < 0) or (y >= 256):

        return 2
    elif  worldMap[y][x] != LAND:
        return 2
    elif  char[y][x]!=-1:
        return 1
    else:
        return 0

#ワールド座標をディスプレイ座標に変換
#def worldToDisplay(x,y):