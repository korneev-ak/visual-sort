

import pygame as pg
import random
import sorts
from inspect import getmembers, isfunction
import UI

class App:
    isLeftDir=False #defines ascending direction of array
    curFunc=None


    sortFuncs=None

    def __init__(self):
        pg.init()
        pg.event.set_allowed(pg.QUIT)
        random.seed(0)

        App.lineColor = pg.Color(15, 170, 170)
        App.backgroundColor = pg.Color(70, 70, 70)
        App.screen = pg.display.set_mode((0, 0), pg.HWSURFACE)
        App.width, App.height = App.screen.get_size()
        App.values = [random.randint(0, App.height) for k in range(800)]

        funcs = [i[0] for i in getmembers(sorts, isfunction)]
        for i in funcs:
            if i == 'isSorted':
                funcs.remove(i)
                break
        App.sortFuncs = [getattr(sorts, i) for i in funcs]

        App.curSort = App.sortFuncs[1]

        App.changeDirBut = UI.Button(App.screen, 700, 8, 200, 50, 'change direction', 30, action=lambda: setattr(App, 'isLeftDir', not (App.isLeftDir)))
        App.start = UI.Button(App.screen, 500, 8, 100, 50, 'start', action=self.startSort)
        App.sortOptions=UI.Dropdown(App.screen, 1000, 8, 150, 70, 'options', options=funcs)
        UI.Text(App.screen,"UI alpha channel",pos=(195,40))
        App.slide = UI.Slider(App.screen, 30, 70, 350, 20, minValue=0, maxValue=255,onDrag=lambda x: setattr(UI.Widget, 'alpha', x))

        App.isRunning = True

    def startSort(self):
        App.values=[random.randint(0, App.height) for k in range(250)]
        App.curFunc=App.sortOptions.getOption()
        getattr(sorts,App.curFunc)(self)

    def run(self):
        self.startSort()
        while App.isRunning:
            self.update()

    def update(self):
        App.screen.fill(App.backgroundColor)
        events= pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                quit();

        self.graphUpdate()
        UI.Text.update()
        UI.Widget.updateWidgets(events)
        pg.display.update()

    def graphUpdate(self):
        for i in range(len(App.values)):
            posX=round(i*(App.width/len(App.values)))
            pg.draw.rect(App.screen, App.lineColor, pg.Rect(App.width-posX-App.width // len(App.values)-1 if App.isLeftDir else posX, App.values[i], App.width // len(App.values) + 1, App.height - App.values[i]))



if __name__ == "__main__":
    App().run()



