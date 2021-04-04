import glm
import ctypes
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Vertex:
    Position = glm.vec3(0)
    Color = glm.vec4(0)
    TexCoords = glm.vec2(0)
    TexIndex = ctypes.c_float.value = 0.0

indices = [Vertex()] * 2


teste = { "def": 123 ,"name": "Adriel" }

teste["Nome"] = "Gabriel"

def pega_nome(nome):
    try:
        return teste[nome]
    except:
        return teste["def"]

nome = pega_nome("Nome")

print(glm.sizeof(glm.vec3(0)))