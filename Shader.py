from OpenGL.GL import *
from glm import *
class Shader:
    def __init__(self,vs: str,fs: str):

        self.ID = 0
        self.UniformLocation = {}

        vertexSource = vs
        fragmentSource = fs

        VertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(VertexShader,vertexSource)

        FragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(FragmentShader,fragmentSource)

        glCompileShader(VertexShader)
        infoLogVert = glGetShaderInfoLog(VertexShader)
        if infoLogVert == "":
            print("Error compiling Vertex Shader: " + str(infoLogVert))

        glCompileShader(FragmentShader)
        infoLogFrag = glGetShaderInfoLog(FragmentShader)
        if infoLogFrag == "":
            print("Error compiling Fragment Shader: " + str(infoLogFrag))
        
        self.ID = glCreateProgram()

        glAttachShader(self.ID,VertexShader)
        glAttachShader(self.ID,FragmentShader)

        glLinkProgram(self.ID)

        glDetachShader(self.ID,VertexShader)
        glDetachShader(self.ID,FragmentShader)
        glDeleteShader(VertexShader)
        glDeleteShader(FragmentShader)

    def SetUniMat4(self, name: str, matrix: mat4):
        self.Bind()
        glUniformMatrix4fv(self.GetUniformLocation(name),1,False,matrix.to_list())

    def Bind(self):
        glUseProgram(self.ID)
    
    def Unbind(self):
        glUseProgram(0)
    
    def GetUniformLocation(self,name: str) -> int:
        try:
            return self.UniformLocation[name]
        except:
            location = glGetUniformLocation(self.ID,name)
            if location == -1:
                print("Warning: uniform '" + name + "' doesn't exist!")
            self.UniformLocation[name] = location
            return location
    
    def Dispose(self):
        glDeleteProgram(self.ID)
    