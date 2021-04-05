from Shader import Shader
from shaders import *
from Render import *
from OpenGL.GL import *
import freetype
from glm import *

class Character:
    def __init__(self,textureID: int, size: vec2, bearing: vec2, advance: int):
        self.TextureID = textureID
        self.Size = size
        self.Bearing = bearing
        self.Advance = advance

class Text:
    def __init__(self,path: str):
        self.characters = {}

        face = freetype.Face(path)
        face.set_pixel_sizes(0,48)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)

        for i in range(0,256,1):
            face.load_char(i) # FT_LOAD_RENDER is the default flag here

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            texId = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D,texId)
            glTexImage2D(GL_TEXTURE_2D, 
                        0, 
                        GL_RED, 
                        face.glyph.bitmap.width ,
                        face.glyph.bitmap.rows, 
                        0, 
                        GL_RED, 
                        GL_UNSIGNED_BYTE,
                        face.glyph.bitmap.buffer )
            
            character = Character(texId,
                                vec2(face.glyph.bitmap.width,face.glyph.bitmap.rows),
                                vec2(face.glyph.bitmap_left,face.glyph.bitmap_top),
                                face.glyph.advance.x)

            self.characters[chr(i)] = character
        
        glBindTexture(GL_TEXTURE_2D,0)
        #TODO: Delete face
    
    #TODO: add a function that return the total size of a text

    def SizePreviw(self,text: str,scale: float) -> float:
        x = 1
        for i in text:
            ch: Character = self.characters[i]
            x += (ch.Advance >> 6) * scale
        return x


    def Draw(self,render: Render2D,text: str, x: float, y: float, scale: float, color: vec4):
        count = 0
        for i in text:
            ch: Character = self.characters[i]

            xpos = x + ch.Bearing.x * scale
            ypos = y - (ch.Size.y - ch.Bearing.y) * scale

            w = ch.Size.x * scale
            h = ch.Size.y * scale
            
            render.DrawQuadTexture(vec2(xpos,ypos + h), vec2(w,-h), ch.TextureID, color)
            x += (ch.Advance >> 6) * scale
            count += 1