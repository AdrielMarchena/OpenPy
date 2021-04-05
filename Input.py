from glm import *
import glfw

class Keyboard:
    clickedControl = [False] * 512
    pressedKey = [False] * 512
    
    #Check if the key is press
    @staticmethod
    def isPress(key: int) -> bool:
        return Keyboard.pressedKey[key]
    
    #Grab only the first click on this key
    @staticmethod
    def clicked(key: int) -> bool:
        if Keyboard.clickedControl[key]:
            return False
        if Keyboard.pressedKey[key]:
            Keyboard.clickedControl[key] = True
            return Keyboard.pressedKey[key]
        return False
    
    #used as callback function on glfw
    @staticmethod
    def handleClicks(window,key: int,scancode,action: int,mods):
        if action == glfw.PRESS:
            Keyboard.pressedKey[key] = True
                
        if action == glfw.RELEASE:
            Keyboard.pressedKey[key] = False
            Keyboard.clickedControl[key] = False
    
#------------------------------------------------------------------------------------------

class Mouse:
    pos = vec2(0)
    prevPos = vec2(0)
    offPos = vec2(0)
    prevOffPos = vec2(0)

    clickedControl = [None] * 16
    pressedKey = [False] * 16
    
    @staticmethod
    def isPress(key: int) -> bool:
        return Mouse.pressedKey[key]

    #Grab only the first click on this key
    @staticmethod
    def clicked(key: int) -> bool:
        if Mouse.clickedControl[key]:
            return False
        if Mouse.pressedKey[key]:
            Mouse.clickedControl[key] = True
            return Mouse.pressedKey[key]
        return False
    
    #used as callback function on glfw
    @staticmethod
    def handleClicks(window,key: int,action: int,mods):
        if action == glfw.PRESS:
            Mouse.pressedKey[key] = True
                
        if action == glfw.RELEASE:
            Mouse.pressedKey[key] = False
            Mouse.clickedControl[key] = False
    
    #used as callback function on glfw
    @staticmethod
    def handleMove(window,xpos: int,ypos: int):
        if Mouse.pos == vec2(xpos,ypos):
            return
        Mouse.prevPos = Mouse.pos
        Mouse.pos = vec2(xpos,ypos)
    
    #used as callback function on glfw
    @staticmethod
    def handleScroll(window,xOffSet: int,yOffSet: int):
        if Mouse.offPos == vec2(xOffSet,yOffSet):
            return
        Mouse.prevOffPos = Mouse.offPos
        Mouse.offPos = vec2(xOffSet,yOffSet)