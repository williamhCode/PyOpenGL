from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

class Shader:
    
    def __init__(self, vertexFilepath, fragmentFilepath):
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER), 
            validate=False
        )
        
        self.ID = shader
        
    def use(self):
        glUseProgram(self.ID)
        
    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.ID, name), value)
        
    def setFloat(self, name, value):
        glUniform1f(glGetUniformLocation(self.ID, name), value)
        
    def setMat4(self, name, value):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_TRUE, np.array(value, dtype=np.float32))
        
    def setVec3(self, name, value):
        glUniform3fv(glGetUniformLocation(self.ID, name), 1, np.array(value, dtype=np.float32))


        