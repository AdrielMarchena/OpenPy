from Input import *
from Render import *
from glm import *
#Playground here

class Game:
    def __init__(self):
        self.running = True
        self.entitys = []
        self.screenSize = vec2(0)
        self.actualScreenSize = vec2()

    def OnAttach(self):
        print("Load resources and create things here, will be called before the loop start")

    def Update(self,deltaTime: float):
        print("implement update here")
        #for i in self.entitys:
            #i.Update()

    def Draw(self,render: Render2D):
        print("implement draw here")
        #for i in self.entitys:
            #i.Draw()
    
    def Dispose(self):
        print("Dispose things here, will be called after the loop ends")

    #Invert y position
    def MousePosC(self) -> vec2:
        #TODO: improve this, for now, work only on the original resolution
        return vec2( Mouse.pos.x, -( Mouse.pos.y - screenSize.y))

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