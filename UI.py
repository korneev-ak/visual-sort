
import pygame as pg



pg.init()



def lambdaWrap(func,args):
    """
    instead of lambdas in loops that don't copy values
    :return: lambda: func(*args)
    """
    return lambda:func(*args)

class Text():
    freeInstances=[]
    __slots__ = ['surface','text','size','pos']
    def __init__(self,surface:pg.Surface,text:str='text',size:int=50,**kwargs):
        self.surface=surface
        self.text=text
        self.size=size
        self.pos=kwargs.get('pos',(self.surface.get_width()//2,self.surface.get_height()//2))
        if kwargs.get('isIndependent',True):
            Text.freeInstances.append(self)

    def draw(self):
        render=pg.font.Font(None,self.size).render(self.text,1,pg.Color(220,220,220))
        render.set_alpha(Widget.alpha)
        self.surface.blit(render,render.get_rect(center=self.pos))

    @staticmethod
    def update():
        for i in Text.freeInstances:
            i.draw()


class Widget():
    alpha=150
    widgets=[]
    __slots__ = ['posX','posY','surface','color','text','background','isHidden']
    def __init__(self,surface:pg.Surface,posX:int=0,posY:int=0,width:int=100,height:int=50,textInput:str='text',textSize:int=30,color:pg.Color=pg.Color(50,50,50),**kwargs):
        Widget.widgets.append(self)
        self.posX=posX
        self.posY=posY
        self.surface=surface
        self.color=color
        self.background=pg.Surface((width,height))
        self.background.set_alpha(Widget.alpha)
        self.background.fill(color)
        self.isHidden=kwargs.get('isHidden',False)
        self.text: Text = Text(self.background,textInput, textSize,isIndependent=False)

    @staticmethod
    def updateWidgets(events:list[pg.event]):
        for widget in Widget.widgets:
            if not(widget.isHidden):
                widget.update(events)

    def update(self,events:list[pg.event]):
        if not(self.isHidden):
            self.text.draw()
            self.background.set_alpha(Widget.alpha)

            self.surface.blit(self.background, (self.posX, self.posY))

    def changeVisibility(self):
        self.isHidden=not(self.isHidden)



class Button(Widget):
    __slots__ = ['action','hoverColor','clickColor']
    def __init__(self,surface:pg.Surface,posX:int=0,posY:int=0,width:int=100,height:int=50,textInput:str='text',textSize:int=30,color:pg.Color=pg.Color(50,50,50),**kwargs):
        super().__init__(surface,posX,posY,width,height,textInput,textSize,color,**kwargs)
        self.action=kwargs.get('action',lambda :print('button click '+'"'+textInput+'"'))
        self.hoverColor=kwargs.get('hoverColor',pg.Color(200,200,200))
        self.clickColor=kwargs.get('clickColor',pg.Color(150,150,150))

    def update(self,events:list[pg.event]):
        isPointed=pg.mouse.get_pos()[0] in range(self.posX,self.posX+self.background.get_width()) and pg.mouse.get_pos()[1] in range(self.posY,self.posY+self.background.get_height())
        if isPointed:
            self.background.fill(self.hoverColor)
        else:
            self.background.fill(self.color)
        if pg.mouse.get_pressed()[0] and isPointed:
            self.background.fill(self.clickColor)

        for event in events:
            if event.type==pg.MOUSEBUTTONDOWN and isPointed:
                self.action()
        super().update(events)

#vertical or horizontal orientation of slider wont swap width and height of block
class Slider(Widget):
    __slots__ = ['onDrag','isVertical','value','minValue','maxValue','handleColor','isMousePressed','handle','handlePos']
    def __init__(self,surface:pg.Surface,posX:int=0,posY:int=0,width:int=200,height:int=30,textInput:str='',textSize:int=30,color:pg.Color=pg.Color(50,50,50),**kwargs):
        super().__init__(surface,posX,posY,width,height,textInput,textSize,color,**kwargs)
        self.onDrag=kwargs.get('onDrag',lambda x:print(x))
        self.isVertical=kwargs.get('isVertical',False)
        self.value=0
        self.minValue=kwargs.get('minValue',0)
        self.maxValue=kwargs.get('maxValue',100)
        self.handleColor=kwargs.get('handleColor',pg.Color(250,250,250))
        self.isMousePressed=False

        if self.isVertical:
            self.handle = pg.Surface((width*2, height//25))
        else:
            self.handle=pg.Surface((width//25,height*2))
        self.handle.set_alpha(Widget.alpha)
        self.handle.fill(self.handleColor)

        if self.isVertical:
            self.handlePos=posY+self.background.get_height()//2
        else:
            self.handlePos = posX + self.background.get_width() // 2


    def update(self,events:list[pg.event]):
        for event in events:
            if event.type==pg.MOUSEBUTTONDOWN and pg.mouse.get_pos()[0] in range(self.posX,self.background.get_width()+self.posX) and pg.mouse.get_pos()[1] in range(self.posY,self.background.get_height()+self.posY):
                self.isMousePressed=True
            if event.type==pg.MOUSEBUTTONUP:
                self.isMousePressed=False
        super().update(events)
        if self.isMousePressed:
            if self.isVertical:
                if pg.mouse.get_pos()[1] in range(self.posY, self.posY + self.background.get_height()):
                    self.handlePos=pg.mouse.get_pos()[1]
                elif pg.mouse.get_pos()[1]<self.posY:
                    self.handlePos=self.posY
                else:
                    self.handlePos=self.posY+self.background.get_height()

                self.value=self.maxValue-((pg.mouse.get_pos()[1]-self.posY)/self.background.get_height())*self.maxValue

            else:
                if pg.mouse.get_pos()[0] in range(self.posX,self.posX+self.background.get_width()):
                    self.handlePos = pg.mouse.get_pos()[0]
                elif pg.mouse.get_pos()[0]<self.posX:
                    self.handlePos=self.posX
                else:
                    self.handlePos=self.posX+self.background.get_width()

                self.value = ((pg.mouse.get_pos()[0] - self.posX) / self.background.get_width()) * self.maxValue
            self.onDrag(self.value)
        if self.isVertical:
            self.surface.blit(self.handle, self.handle.get_rect(center=(self.background.get_width() // 2 + self.posX, self.handlePos)))
        else:
            self.surface.blit(self.handle, self.handle.get_rect(center=(self.handlePos, self.background.get_height() // 2 + self.posY)))

class Dropdown(Button):
    __slots__ = ['options','curOption','isExpanded']
    def __init__(self,surface:pg.Surface,posX:int=0,posY:int=0,width:int=100,height:int=50,textInput:str='text',textSize:int=30,color:pg.Color=pg.Color(50,50,50),**kwargs):
        self.options = []
        kwargs.setdefault('action', self.changeItemsVisibility)
        super().__init__(surface, posX, posY, width, height, textInput, textSize, color, **kwargs)

        count = 0
        names = kwargs.get('options')
        self.curOption=names[0]
        self.text.text=self.curOption
        for i in names:
            self.options.append(Button(surface, posX, posY + self.background.get_height() + 50 * count, self.background.get_width(), 50,i, isHidden=True,action=lambdaWrap(setattr,(self,'curOption',i))))

            count += 1
        self.isExpanded = False

    def changeItemsVisibility(self):
        for i in self.options:
            i.changeVisibility()

    def update(self,events:list[pg.event]):
        self.text.text=self.curOption
        super().update(events)

    def getOption(self):
        return self.curOption



