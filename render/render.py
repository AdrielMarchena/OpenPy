from glm import *
import ctypes
import OpenGL
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy
from PIL import Image

from render.shader import Shader
from render.textures import Texture, SubTexture

sizeOfFloat = ctypes.sizeof(GLfloat)
sizeOfInt = ctypes.sizeof(GLint)

class Vertex:
    Position = vec3()
    Color = vec4()
    TexCoords = vec2()
    TexIndex = 1.0

    def __init__(self):
        self.Position = vec3()
        self.Color = vec4()
        self.TexCoords = vec2()
        self.TexIndex = 0.0

    def Raw(self):
        vert = [self.Position.x,self.Position.y,self.Position.z,
                self.Color.x,self.Color.y,self.Color.z,self.Color.w,
                self.TexCoords.x,self.TexCoords.y,
                self.TexIndex]
        return vert

class Render2D:
    def __init__(self,vs: str,fs: str,MaxText=8):
        self.MaxQuadCount = 2000
        self.MaxVertexCount = self.MaxQuadCount * 4
        self.MaxIndexCount = self.MaxQuadCount * 6
        self.MaxTextures = MaxText
        self.QuadVA = 0
        self.QuadVB = 0
        self.QuadIB = 0
        self.WhiteTexture = 0 #The first texture unit is reserv for a 1x1 white texture
        self.IndexCount = 0
        self.QuadBuffer = [Vertex()]
        self.QuadBufferPtr = 0
        self.TextureSlots = [0] * self.MaxTextures        
        self.TextureSlotIndex = 1
        self.TexCoords = [vec2(0,0), vec2(1,0), vec2(1,1), vec2(0,1)]
        self.shader = Shader(vs,fs)

        print("Texture Units: " + str(self.MaxTextures))

        self.QuadVA = glGenVertexArrays(1)
        glBindVertexArray(self.QuadVA)

        self.QuadVB = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.QuadVB)
        glBufferData(GL_ARRAY_BUFFER, self.MaxVertexCount * 10 * sizeOfFloat, None, GL_DYNAMIC_DRAW)

        #Layout Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,3,GL_FLOAT, GL_FALSE, 10*sizeOfFloat,ctypes.c_void_p(0)) #The last parm is the offset, can't find a offset function
        
        #Layout Color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,4,GL_FLOAT, GL_FALSE, 10*sizeOfFloat,ctypes.c_void_p(12))

        #Layout TexCoords
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2,2,GL_FLOAT, GL_FALSE, 10*sizeOfFloat,ctypes.c_void_p(28))

        #Layout TexIndex
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3,1,GL_FLOAT, GL_FALSE, 10*sizeOfFloat,ctypes.c_void_p(36))
        
        self.shader.Bind()
        loc = self.shader.GetUniformLocation("u_Textures")
        samplers = []
        for i in range(0,self.MaxTextures,1):
            samplers.append(i)
        glUniform1iv(loc, self.MaxTextures ,numpy.array(samplers,dtype=numpy.int32))

        indices = [0] * self.MaxIndexCount
        offset = 0
        for i in range(0,self.MaxIndexCount,6):
            indices[i + 0] = 0 + offset
            indices[i + 1] = 1 + offset
            indices[i + 2] = 2 + offset

            indices[i + 3] = 2 + offset
            indices[i + 4] = 3 + offset
            indices[i + 5] = 0 + offset

            offset += 4
        
        self.QuadIB = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.QuadIB)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,size=None,data=numpy.array(indices,dtype=numpy.uint32),usage=GL_STATIC_DRAW)

        self.WhiteTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.WhiteTexture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        white_color = [[255,255,255,255]]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, white_color)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

        self.TextureSlots[0] = self.WhiteTexture
        for i in range(1,self.MaxTextures,1):
            self.TextureSlots[i] = 0
        
    def ShutDown(self):
        glDeleteVertexArrays(1,self.QuadVA)
        glDeleteBuffers(1,self.QuadVB)
        glDeleteBuffers(1,self.QuadIB)
        glDeleteTextures(1,self.WhiteTexture)
    
    def BeginBatch(self):
        self.QuadBuffer = []
        self.QuadBufferPtr = 0

    def ToRaw(self):
        ret = []
        for i in range(0,self.QuadBufferPtr,1):
            ret.extend(self.QuadBuffer[i].Raw())
        return ret
    
    def EndBatch(self):
        glBindBuffer(GL_ARRAY_BUFFER,self.QuadVB)
        data = numpy.array(self.ToRaw(),dtype=numpy.float32)
        glBufferSubData(GL_ARRAY_BUFFER,0,size=None,data=data)
    
    def BindShader(self):
        self.shader.Bind()
    
    def UnbindShader(self):
        self.shader.Unbind()

    def Flush(self):
        self.shader.Bind()
        for i in range(0,self.TextureSlotIndex,1):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D,self.TextureSlots[i])
        
        glBindVertexArray(self.QuadVA)
        glDrawElements(GL_TRIANGLES,self.IndexCount,GL_UNSIGNED_INT,None)

        self.IndexCount = 0
        self.TextureSlotIndex = 1
    
    def FillVertices(self,position: vec2,size: vec2,color: vec4,texCoords: list,texIndex: float, rotation=None, axis=None):
        
        quadVertices = [
            vec3(position.x,position.y,0.0),
            vec3(position.x + size.x,position.y,0.0),
            vec3(position.x + size.x,position.y + size.y,0.0),
            vec3(position.x,position.y + size.y,0.0)
        ]
        
        if rotation != None:
            if axis == None:
                axis = vec3(0.0,0.0,1.0)
            quadVertices = self.RotateVertices(quadVertices,rotation,vec3(position.x + (size.x / 2), position.y + (size.y / 2), 0.0), axis)

        v = Vertex()
        v.Position = quadVertices[0]
        v.Color = color
        v.TexCoords = texCoords[0]
        v.TexIndex = texIndex
        self.QuadBuffer.append(v)
        self.QuadBufferPtr += 1

        f = Vertex()
        f.Position = quadVertices[1]
        f.Color = color
        f.TexCoords = texCoords[1]
        f.TexIndex = texIndex
        self.QuadBuffer.append(f)
        self.QuadBufferPtr += 1

        g = Vertex()
        g.Position = quadVertices[2]
        g.Color = color
        g.TexCoords = texCoords[2]
        g.TexIndex = texIndex
        self.QuadBuffer.append(g)
        self.QuadBufferPtr += 1

        h = Vertex()
        h.Position = quadVertices[3]
        h.Color = color
        h.TexCoords = texCoords[3]
        h.TexIndex = texIndex
        self.QuadBuffer.append(h)
        self.QuadBufferPtr += 1
    
    def RotateVertices(self,vertices: list,angle: float,rotationCenter: vec3,axis: vec3):
        
        translationMatrix = translate(identity(mat4), rotationCenter - (rotationCenter*2))
        rotationMatrix = rotate(identity(mat4),angle,axis)
        reverseTranslationMatrix = translate(identity(mat4),rotationCenter)

        for i in range(0,4,1):
            vertices[i] = vec3(reverseTranslationMatrix * rotationMatrix * translationMatrix * vec4(vertices[i],1.0))
        
        return vertices
    
    def DrawQuad(self, position: vec2, size: vec2, color: vec4,rotation=None,axis=None):
        
        if self.IndexCount >= self.MaxIndexCount:
            self.EndBatch()
            self.Flush()
            self.BeginBatch()
        
        textureIndex = 0.0

        self.FillVertices(position,size,color,self.TexCoords,textureIndex,rotation,axis)
        self.IndexCount += 6
    
    def DrawQuadTexture(self,position: vec2,size: vec2,texId: int,color=vec4(1),rotation=None,axis=None):
        if self.IndexCount >= self.MaxIndexCount or self.TextureSlotIndex > self.MaxTextures - 1:
            self.EndBatch()
            self.Flush()
            self.BeginBatch()
        
        tx = self.TexCoords

        #if it's a Texture get texID
        if isinstance(texId,Texture):
            texId = texId.TexID
        
        #if it's a SubTexture get TexCoords and texID
        if isinstance(texId,SubTexture):
            tx = texId.TexCoords
            texId = texId.TexID

        textureIndex = 0

        #Look if this texture already exist in the current batch
        for i in range(1,self.TextureSlotIndex,1):
            if self.TextureSlots[i] == texId:
                textureIndex = float(i)
                break
        
        if textureIndex == 0:
            textureIndex = float(self.TextureSlotIndex)
            self.TextureSlots[self.TextureSlotIndex] = texId
            self.TextureSlotIndex += 1
        
        self.FillVertices(position,size,color,tx,textureIndex,rotation,axis)
        self.IndexCount += 6