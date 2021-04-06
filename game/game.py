from game.input import Keyboard, Mouse
from render.render import Render2D
from glm import *
from render.text import Text
from api.api import API
from utils.parse_folder import parse_folder
#Playground here

class BoxItem:
    def __init__(self,index: int,label: str,value,xsize: float,scale=1):
        self.index = index
        self.label = label
        self.value = value
        self.xsize = xsize
        self.scale = scale

class BoxList:
    def __init__(self,pos: vec2,size: vec2,color: vec4,list_itens: dict,font: Text,scale=1):
        self.color = color
        self.pos = pos
        self.size = size
        self.itens = list_itens
        self.box_list = []
        self.currentItem = None
        self.itemSize = vec2(50)
        self.font = font
        self.scale = scale
        self.biggerX = self.size.x
        self.api: API = None
        count = 1
        for i in self.itens:
            x = font.SizePreviw(i,self.scale)
            last = None
            if x > self.biggerX:
                self.biggerX = x
            self.box_list.append(BoxItem(count,i,self.itens[i],x,self.scale))
            count += 1
        
        self.currentItem = self.box_list[0]
    
    def Update(self,deltaTime: float):
        for it in self.box_list:
            if self.api.point_vs_rect(Mouse.pos.x,Mouse.pos.y,self.pos.x,self.pos.y + (it.index * self.itemSize.y),it.xsize,self.itemSize.y):
                if Mouse.clicked(0):
                    self.currentItem = it

    def Draw(self,render: Render2D):
        render.DrawQuad(vec2(self.pos.x - self.biggerX/4,self.pos.y),vec2(self.biggerX * 1.5 ,self.size.y),self.color)
        for it in self.box_list:
            if self.api.point_vs_rect(Mouse.pos.x,Mouse.pos.y,self.pos.x,self.pos.y + (it.index * self.itemSize.y),it.xsize,self.itemSize.y):
                render.DrawQuad(vec2(self.pos.x,self.pos.y + (it.index * self.itemSize.y)), vec2(it.xsize,self.itemSize.y),vec4(0.9,0.6,0.3,1))

    def DrawT(self,render: Render2D):
        for it in self.box_list:
            self.font.Draw(render,it.label,self.pos.x,self.pos.y + (it.index * self.itemSize.y),self.scale,vec4(1))

class Game:
    def __init__(self):
        self.running = True
        self.entitys = []
        self.screenSize = vec2(0)
        self.api: API = None

    def OnAttach(self):
        #Load resources and create things here, will be called before the loop start
        self.fonts = parse_folder("fonts/",".ttf")
        for t in self.fonts:
            self.fonts[t] = Text("fonts/" + str(self.fonts[t]))
        self.Box = BoxList(vec2(200,0),vec2(50,600),vec4(0.2,0.6,0.9,1),self.fonts,self.fonts["comic"])
        self.Box.api = self.api

    def Update(self,deltaTime: float):
        self.Box.Update(deltaTime)
        #for i in self.entitys:
            #i.Update()

    def Draw(self,render: Render2D):
        self.Box.Draw(render)
        w = self.Box.currentItem.value.SizePreviw("ANTONIO BUNDA MOLE",0.5)
        if self.api.point_vs_rect(Mouse.pos.x,Mouse.pos.y,self.screenSize.x/2,self.screenSize.y/2,w,50):
            render.DrawQuad(vec2(self.screenSize.x/2,self.screenSize.y/2),vec2(w,45),vec4(1.0))
        #for i in self.entitys:
            #i.Draw()
    
    def DrawT(self,render: Render2D):
        self.Box.DrawT(render)
        self.Box.currentItem.value.Draw(render,"ANTONIO BUNDA MOLE",self.screenSize.x/2,self.screenSize.y/2,0.5,vec4(0.2,0.6,0.9,1))

    def Dispose(self):
        for t in self.fonts:
            self.fonts[t].Dispose()
            print("Dispose things here, will be called after the loop ends")

    #event's
    def on_resize(self,w: int,h: int):
        print(f"From game, i say that the window resized to W {w} and H {h}")
    
    def on_cursor_move(self,xpos: int,ypos: int):
        print(f"From game, i say that the mouse moved to X {xpos} and Y {ypos}")
    
    def on_mouse_scroll(self,xOffSet: int,yOffSet: int):
        print(f"From game, i say that the mouse scroll to X {xOffSet} and Y {yOffSet}")
    
    def on_mouse_click(self,key,action,mods):
        print(f"From game, i say that the mouse clicked to key {key} and as {action}")
    
    def on_keyboard_click(self,key,scancode,action,mods):
        print(f"From game, i say that the keyboard clicked to key {key} and as {action}")