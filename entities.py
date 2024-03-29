from OpenGL.GL import *
import glm

from models import Model, ColoredCube, TexturedModel
from shader import Shader

from typing import Sequence

class Entity:
    
    def __init__(self, model: Model | TexturedModel, position: Sequence, orientation: Sequence, scale: float):
        """
        Args:
            model (Model): the assiciated model
            position (Sequence): x, y, z position
            orientation (Sequence): pitch, yaw, roll
            scale (float): float
        """
        self.model = model
        self.position = glm.vec3(*position)
        self.orientation = glm.vec3(*orientation)
        self.scale = scale
        self.transform_matrix = self.calculate_transform_matrix()
        
    def calculate_transform_matrix(self):
        pitch = glm.rotate(glm.radians(self.orientation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(glm.radians(self.orientation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(glm.radians(self.orientation.z), glm.vec3(0, 0, 1))
        rotation_transformation = yaw @ pitch @ roll

        position_transformation = glm.translate(self.position)
        
        scale_transformation = glm.scale(glm.vec3(self.scale, self.scale, self.scale))

        transformation_matrix = position_transformation @ rotation_transformation @ scale_transformation
        return transformation_matrix
    
    def update(self):
        pass
        
    def update_transform(self):
        self.transform_matrix = self.calculate_transform_matrix()
        
    def draw(self):
        self.model.draw(self.transform_matrix)
        
    def destroy(self):
        self.model.destroy()


class DirLight():
    def __init__(self, shader: Shader, direction: Sequence, ambient: Sequence, diffuse: Sequence, specular: Sequence):
        self.shader = shader
        self.direction = glm.vec3(*direction)
        self.ambient = glm.vec3(ambient)
        self.diffuse = glm.vec3(diffuse)
        self.specular = glm.vec3(specular)
        
    def update(self):
        self.shader.use()
        
        self.shader.set_vec3("dirLight.direction", self.direction)
        
        self.shader.set_vec3("dirLight.ambient", self.ambient)
        self.shader.set_vec3("dirLight.diffuse", self.diffuse)
        self.shader.set_vec3("dirLight.specular", self.specular)
        

class PointLight(Entity):
    CONSTANT = 1.0
    LINEAR = 0.00
    QUADRATIC = 0.00
    
    def __init__(self, shaders: Sequence[Shader], color: Sequence, position: Sequence, index: int):
        """
        Args:
            shaders (Sequence[Shader]): cube shader and point light shader
            color (Sequence): r, g, b color (0.0 - 1.0)
            position (Sequence): x, y, z position
            index (int): index of point light
        """
        super().__init__(ColoredCube(*color, shaders[0]), position, [0, 0, 0], 0.2)
        
        self.color = glm.vec3(*color)
        self.shader = shaders[1]
        self.index = index
        
    def update(self):
        self.shader.use()

        self.shader.set_vec3(f"pointLights[{self.index}].position", self.position)
        
        self.shader.set_float(f"pointLights[{self.index}].constant", PointLight.CONSTANT)
        self.shader.set_float(f"pointLights[{self.index}].linear", PointLight.LINEAR)
        self.shader.set_float(f"pointLights[{self.index}].quadratic", PointLight.QUADRATIC)
        
        self.shader.set_vec3(f"pointLights[{self.index}].ambient", self.color * 0.0)
        self.shader.set_vec3(f"pointLights[{self.index}].diffuse", self.color)
        self.shader.set_vec3(f"pointLights[{self.index}].specular", self.color)
