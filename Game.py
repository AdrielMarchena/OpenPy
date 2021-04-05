from Input import *
from Render import *
from glm import *
from Text import Text
from API import API
#Playground here

class Game:
    def __init__(self):
        self.running = True
        self.entitys = []
        self.screenSize = vec2(0)
        self.API: API = None

    def OnAttach(self):
        #Load resources and create things here, will be called before the loop start
        #TODO: add all fonts on the folder here
        self.fonts = {
            "arial": Text("fonts/arial.ttf"),
            "arialbd": Text("fonts/arialbd.ttf"),
            "arialbi": Text("fonts/arialbi.ttf"),
            "ariali": Text("fonts/ariali.ttf"),
            "comic_sans": Text("fonts/comic.ttf"),
            
        }

    def Update(self,deltaTime: float):
        print("implement update here")
        #for i in self.entitys:
            #i.Update()

    def Draw(self,render: Render2D):
        w = self.fonts["comic_sans"].SizePreviw("Teste Foda",1)
        if self.API.point_vs_rect(Mouse.pos.x,Mouse.pos.y,self.screenSize.x/2,self.screenSize.y/2,w,50):
            render.DrawQuad(vec2(self.screenSize.x/2,self.screenSize.y/2),vec2(w,45),vec4(1.0))
        #for i in self.entitys:
            #i.Draw()
    
    def DrawT(self,render: Render2D):
        self.fonts["comic_sans"].Draw(render,"Teste Foda",self.screenSize.x/2,self.screenSize.y/2,1,vec4(0.2,0.6,0.9,1))

    def Dispose(self):
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