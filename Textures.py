from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
from PIL import Image
from glm import *
class Texture:
    def __init__(self,path: str):
        
        self.TexID = 0
        self.Wid = 0
        self.Hei = 0

        self.TexID = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.TexID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        self.Wid, self.Hei = image.size

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.Wid, self.Hei, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
    
    def Dispose(self):
        glDeleteTextures(1,self.TexID)

    def Bind(self):
        glBindTexture(GL_TEXTURE_2D,self.TexID)
    
    def Unbind(self):
        glBindTexture(GL_TEXTURE_2D,0)


class SubTexture:
    def __init__(self,texID: int, min: vec2, max: vec2):
        self.TexID = texID
        self.TexCoords = []
        if texID != 0:
            self.TexCoords = [vec2()] * 4
            self.TexCoords[0] = vec2(min.x,min.y)
            self.TexCoords[1] = vec2(max.x,min.y)
            self.TexCoords[2] = vec2(max.x,max.y)
            self.TexCoords[3] = vec2(min.x,max.y)
    
#usage: SubTexture.CreateFromCoords(texID,vec2(128,128),vec2(1,1),vec2(32,32))
def CreateSubTexFromCoords(texID,size,coords,spriteSize) -> SubTexture:
    sheetWid = size.x
    sheetHei = size.y
    min = vec2( (coords.x * spriteSize.x) / sheetWid, (coords.y * spriteSize.y) / sheetHei)
    max = vec2( ((coords.x + 1) * spriteSize.x) / sheetWid, ((coords.y + 1) * spriteSize.y) / sheetHei)
    return SubTexture(texID,min,max)
