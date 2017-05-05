from variable import(
idList,
actors,
)
def getNewId():
    for i,id in enumerate(idList):
        if id==0:
            idList[i] = 1
            return i
    print "too many objects"
    return -1


def getIdFromPos(x,y):
    for actor in actors:
        if actor.x==x and actor.y==y:
            return actor.id
    return -1

