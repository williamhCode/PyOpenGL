from OpenGL.GL import *
import numpy as np
import glm

from shader import Shader

class Camera:
    # camera faces in the direction of the negative z-axis
    forward = glm.vec3(0.0, 0.0, -1.0)
    up = glm.vec3(0.0, 1.0, 0.0)
    
    def __init__(self, position: list, orientation: list, fov, aspect_ratio, near, far):
        self.position = glm.vec3(*position)
        # orientation is a list of euler angles (yaw, pitch, roll)
        self.orientation = glm.vec3(*orientation)
        self.projection_transform = glm.perspective(fov, aspect_ratio, near, far)
        
    def rotate(self, pitch, yaw, roll):
        self.orientation.x += pitch
        self.orientation.y += yaw
        self.orientation.z += roll
        
    def translate(self, x, y, z):
        self.position.x += x
        self.position.y += y
        self.position.z += z
        
    def update(self, shaders: list[Shader]):
        pitch = glm.rotate(glm.radians(self.orientation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(glm.radians(self.orientation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(glm.radians(self.orientation.z), glm.vec3(0, 0, 1))
        
        rotation_transformation = yaw @ pitch @ roll
        
        forward = rotation_transformation @ self.forward
        up = rotation_transformation @ self.up
        
        lookat_matrix = glm.lookAt(self.position, self.position + forward, up)
        
        projView_matrix = self.projection_transform @ lookat_matrix
        
        for shader in shaders:
            shader.use()
            shader.setMat4("projView", projView_matrix)
            shader.setVec3("viewPos", self.position)
        
class FPS_Camera(Camera):
    
    def rotate(self, horizontal, vertical):
        super().rotate(vertical, horizontal, 0)
        self.orientation.x = max(-90, min(self.orientation.x, 90))
    
    def move(self, forwards, sideways, vertical):
        move_direction = glm.rotateY(glm.vec3(sideways, vertical, -forwards), glm.radians(self.orientation.y))
        self.translate(*move_direction)