from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

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
        
    def set_int(self, name, value):
        glUniform1i(glGetUniformLocation(self.ID, name), value)
        
    def set_float(self, name, value):
        glUniform1f(glGetUniformLocation(self.ID, name), value)
        
    def set_vec2(self, name, value):
        glUniform2fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(value))
        
    def set_vec3(self, name, value):
        glUniform3fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(value))
        
    def set_mat2(self, name, value):
        glUniformMatrix2fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(value))
        
    def set_mat3(self, name, value):
        glUniformMatrix3fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(value))
        
    def set_mat4(self, name, value):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(value))

        