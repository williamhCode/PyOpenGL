from OpenGL.GL import *
import pygame

class Material:
    
    def __init__(self, *filepaths):
        self.textures = tuple(self.generate_texture(filepath) for filepath in filepaths)
        
    def generate_texture(self, filepath):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pygame.image.load(filepath).convert()
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, 'RGBA')

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                     image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)  

        glGenerateMipmap(GL_TEXTURE_2D)
        
        return texture

    def use(self):
        for i, texture in enumerate(self.textures):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, texture)

    def destroy(self):
        glDeleteTextures(len(self.textures), self.textures)
