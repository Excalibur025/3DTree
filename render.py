import os
import pygame
# You might need to install pygame lib, PyOpenGL and PyOpenGL_accelerate?
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

# Function to draw a cube
def draw_cube(x, y, z):
    vertices = [
        (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
        (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    glPushMatrix()
    glTranslatef(x, y, z)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()

# Recursively draw the directory structure
def draw_directory(path, depth=0, x=0, y=0, z=0):
    if depth > 3:  # Limit depth for simplicity
        return
    items = os.listdir(path)
    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            draw_cube(x, y - i, z - depth)
            draw_directory(item_path, depth + 1, x, y - i, z - depth - 2)
        else:
            draw_cube(x + 1, y - i, z - depth)

# Prompt the user for the directory path
directory_path = input("Enter the directory path to visualize: ")

# Variables for rotation
x_rotation = 0
y_rotation = 0
z_translation = -20

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                y_rotation -= 5
            elif event.key == pygame.K_RIGHT:
                y_rotation += 5
            elif event.key == pygame.K_UP:
                x_rotation -= 5
            elif event.key == pygame.K_DOWN:
                x_rotation += 5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, z_translation)
    glRotatef(x_rotation, 1, 0, 0)
    glRotatef(y_rotation, 0, 1, 0)
    
    draw_directory(directory_path)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
