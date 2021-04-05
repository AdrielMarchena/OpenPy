import glfw
from glm import *
import OpenGL
from OpenGL.GL import *
from Render import Render2D
from shaders import *
from Input import *
from API import *
from ctypes import *

from Game import Game
screenSize = vec2(1024,768)
#used for mouse cursor position things
actualScreenSize = vec2(1024,768)

class Window:
    def __init__(self,w: int,h: int,title: str):
        self.w = w
        self.h = h
        self.title = title
        self.API = API()
        screenSize = vec2(w,h)

        if not glfw.init():
            return
        
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE,glfw.TRUE)

        self.window = glfw.create_window(w,h,title,None,None)
        if not self.window:
            glfw.terminate()
            return
        
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        value = [0]

        MaxTextures = glGetInteger(GL_MAX_TEXTURE_UNITS,value)
        self.render = Render2D(VertexShader(),FragmentShader(MaxTextures),MaxTextures)
        self.text_render = Render2D(VertexShaderText(),FragmentShaderText(MaxTextures),MaxTextures)

        self.game = Game()
        self.game.screenSize = screenSize

        #callback functions
        def resize_callback(window,w,h):
            ap = w / h
            actualScreenSize = vec2(w,h)
            glViewport(w//2 - int(screenSize.x//2) ,h//2 - int(screenSize.y//2),int(screenSize.x),int(screenSize.y))
            self.game.on_resize(w,h)
            
        #TODO: Maybe pass the Mouse and Keyboard to Game, maybe
        def on_mouse_scroll_callback(window,xOffSet,yOffSet):
            Mouse.handleScroll(window,xOffSet,yOffSet)
            self.game.on_mouse_scroll(xOffSet,yOffSet)

        def on_cursor_move_callback(window,xpos,ypos):
            Mouse.handleMove(window,xpos,ypos)
            self.game.on_cursor_move(xpos,ypos)
        
        def on_mouse_button_callback(window,key,action,mods):
            Mouse.handleClicks(window,key,action,mods)
            self.game.on_mouse_click(key,action,mods)

        def on_keyboard_click_callback(window,key,scancode,action,mods):
            Keyboard.handleClicks(window,key,scancode,action,mods)
            self.game.on_keyboard_click(key,scancode,action,mods)

        #Set callbacks from glfw
        glfw.set_window_size_callback(self.window,resize_callback)
        glfw.set_scroll_callback(self.window,on_mouse_scroll_callback)
        glfw.set_cursor_pos_callback(self.window,on_cursor_move_callback)
        glfw.set_mouse_button_callback(self.window,on_mouse_button_callback)
        glfw.set_key_callback(self.window,on_keyboard_click_callback)
        
    def Run(self):
        glClearColor(0.2,0.2,0.2,1.0)

        deltaTime = 0.0
        lt = 0.0
        quadColor = vec4(0.0,1.0,1.0,0.5)
        secQuadColor = vec4(0.5,0.5,0.5,1.0)

        self.render.shader.SetUniMat4("u_ViewProj",identity(mat4)) #Camera projection here
        self.render.shader.SetUniMat4("u_Transform", ortho(0.0,screenSize.x,0.0,screenSize.y,-1.0,1.0))

        self.text_render.shader.SetUniMat4("u_ViewProj",identity(mat4))
        self.text_render.shader.SetUniMat4("u_Transform", ortho(0.0,screenSize.x,0.0,screenSize.y,-1.0,1.0))

        self.game.OnAttach()
        while not glfw.window_should_close(self.window):

            #Update the window size
            self.w = actualScreenSize.x
            self.h = actualScreenSize.y
            self.game.actualScreenSize = actualScreenSize

            #Calculate DeltaTime
            currentTime = glfw.get_time()
            deltaTime = currentTime - lt
            lt = currentTime

            #Clear the screen
            glClear(GL_COLOR_BUFFER_BIT)

            #Bind Shader and Start a Batch
            self.render.BindShader()
            self.render.BeginBatch()

            #Update Here
            self.game.Update(deltaTime)

            #Draw Here
            self.game.Draw(self.render)
            
            #End the Batch and Flush whaever is there
            self.render.EndBatch()
            self.render.Flush()

            #TODO: add the text draw rotine here, need to be here because it use other shader and other batch
            self.text_render.BindShader()
            self.text_render.BeginBatch()
            
            self.game.DrawT(self.text_render)

            self.text_render.EndBatch()
            self.text_render.Flush()

            #Swap buffers and do the window event stuff
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        
        self.game.Dispose()
        glfw.terminate()
