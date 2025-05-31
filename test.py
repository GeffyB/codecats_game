# pyright: reportUndefinedVariable=false


import pgzrun

def draw():
    screen.clear()
    screen.blit("tile_floor", (100, 100))

pgzrun.go()
