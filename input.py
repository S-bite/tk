#coding:utf-8
import os
import sys

class key:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def getInput(self):
        res=[]
        while True:
            k=self.impl()
            res.append(k)
            if not ord(k)in [27,91]:
                break
        return res
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


if __name__=="__main__":
    print("in input.py")
    while True:
        getch = key()
        x = getch.getInput()
        print(x)
        if x==[b"q"]:
            break