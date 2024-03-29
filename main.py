import pygame
from pygame.locals import *

from OpenGL.GL import *

import glm
from timer import Timer

from models import *
from material import *
from camera import *
from shader import *
from entities import *
from post_processing import *

def main():
    # initialize -------------------------------------------------- #
    pygame.init()

    # specify opengl version
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )

    # create window
    WIN_SIZE = (1200, 800)
    pygame.display.set_mode((WIN_SIZE), DOUBLEBUF | OPENGL)
    pygame.mouse.set_pos(WIN_SIZE[0]/2, WIN_SIZE[1]/2)
    # pygame.mouse.set_visible(False)
    mouse_inside = False
    
    # initialize opengl
    glClearColor(0.0, 0.0, 0.0, 1)
    glEnable(GL_DEPTH_TEST)
    
    # glCullFace(GL_BACK)
    # glFrontFace(GL_CCW)
    
    # initialize game objects -------------------------------------------------- #
    # shaders
    shader = Shader("shaders/vertex.vert", "shaders/fragment.frag")
    shader.use()
    shader.set_int("material.diffuse", 0)
    shader.set_int("material.specular", 1)
    shader.set_float("material.shininess", 32.0)
    
    shaderBasic = Shader("shaders/simple_3d_vertex.vert", "shaders/simple_3d_fragment.frag")
    
    shader2d = Shader("shaders/screen_vertex.vert", "shaders/screen_fragment.frag")
    
    # post processing
    post_processing = PostProcessing(WIN_SIZE, shader2d)

    # objects
    backpack_model = OBJModel("models/backpack.obj", Material("img/diffuse.jpg", "img/specular.jpg"), shader)
    backpack = Entity(backpack_model, (0, 0, 0), (0, 0, 0), 0.5)
    
    textured_cube_model = TexturedCube(Material("img/crate_diffuse.jpg", "img/crate_specular.jpg"), shader)
    cube = Entity(textured_cube_model, (0, 0, 0), (0, 0, 0), 1)
    
    # lights
    dir_light = DirLight(shader, (0.5, -1, -0.5), (0.2, 0.2, 0.2), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0))
    
    point_lights = [
        PointLight((shaderBasic, shader), (1.0, 0.0, 0.0), (1.0, 1.0, 1.0), 0),
        PointLight((shaderBasic, shader), (0.0, 1.0, 0.0), (1.0, 1.0, -1.0), 1),
        PointLight((shaderBasic, shader), (0.0, 0.0, 1.0), (-1.0, 1.0, 1.0), 2),
    ]

    static_entities: list[Entity] = []
    dynamic_entites: list[Entity] = [backpack]
    
    camera = FPS_Camera([0.0, 0.0, 5.0], [0.0, 0.0, 0.0], glm.radians(45.0), WIN_SIZE[0]/WIN_SIZE[1], 0.3, 30.0)
    
    # game loop -------------------------------------------------- #
    clock = Timer()

    running = True
    while running:
        # timing -------------------------------------------------- #
        dt = clock.tick()

        framerate = clock.get_fps()
        pygame.display.set_caption(f"Running at {framerate :.2f} fps.")

        # check events -------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        X_CENTER = WIN_SIZE[0]/2
        Y_CENTER = WIN_SIZE[1]/2
        # mouse movement
        if mouse_inside == False:
            if pygame.mouse.get_focused():
                pygame.mouse.set_pos((X_CENTER, Y_CENTER))
                mouse_inside = True
        else:
            x, y = pygame.mouse.get_pos()

            yaw_increment = 0.1 * (X_CENTER - x)
            pitch_increment = 0.1 * (Y_CENTER - y)

            camera.rotate(yaw_increment, pitch_increment)

            pygame.mouse.set_pos((X_CENTER, Y_CENTER))

        # key press
        forwards = 0.0
        sideways = 0.0
        vertical = 0.0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            sideways -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            sideways += 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            forwards += 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            forwards -= 5
        if keys[pygame.K_SPACE]:
            vertical += 5
        if keys[pygame.K_LSHIFT]:
            vertical -= 5

        camera.move(dt * forwards, dt * sideways, dt * vertical)

        # update objects -------------------------------------------------- #
        camera.update([shader, shaderBasic])
        
        dir_light.update()
        
        # backpack.orientation.y += 50 * dt
        
        for point_light in point_lights:
            point_light.update()
        
        for entity in dynamic_entites:
            entity.update()
        
        for entity in dynamic_entites:
            entity.update_transform()

        # drawing
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # post_processing.begin()

        glDisable(GL_CULL_FACE)
        for point_light in point_lights:
            point_light.draw()
        
        glEnable(GL_CULL_FACE)
        for entity in dynamic_entites:
            entity.draw()
        
        for entity in static_entities:
            entity.draw()

        # post_processing.end()

        # flip screen
        pygame.display.flip()

    # cleanup -------------------------------------------------- #
    for entity in dynamic_entites:
        entity.destroy()
        
    for entity in static_entities:
        entity.destroy()

main()
pygame.quit()
quit()
