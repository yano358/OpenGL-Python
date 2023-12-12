import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos , pi, pow
import random
from numpy import cross, linalg, zeros

viewer = [0.0, 0.0, 10.0]
theta = 0.0
pix2angle = 1.0
phi = 0.0
piy2angle = 1.0
left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0, 0.7, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 0.5, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 15.0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.2, 8.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.7, 0.2, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 10.0, 1.0])
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.9)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.005)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def shutdown():
    pass

def spin (angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)
 
n = 15
matrix = zeros((n+1,n+1,3))
matrixWithVectors = zeros((n+1,n+1,3))

def render(time):
    global theta
    global phi
     
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    spin(time*180/pi)
    drawEggTriangles()
    glFlush()

def matrixValues():
    for i in range (0, n + 1):
        for j in range (0, n + 1):
            u = i/n
            v = j/n
            matrix[i][j][0] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * cos(pi * v)
            matrix[i][j][1] =  160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2)
            matrix[i][j][2] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * sin(pi * v)

def calculate_normal(v1, v2, v3):
    vector1 = v2 - v1
    vector2 = v3 - v1

    cross_product = cross(vector1, vector2)

    # Normalize
    normal = cross_product / linalg.norm(cross_product)

    return normal

            
def drawEggTriangles(): 
    for i in range (0, n):
        for j in range (0, n):
            glBegin(GL_TRIANGLES)
            glNormal3f(calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[0], calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[1], calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[2])
            glVertex3f(matrix[i][j][0], matrix[i][j][1] - 5, matrix[i][j][2])
            
            glNormal3f(calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[0], calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[1], calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[2])
            glVertex3f(matrix[i + 1][j][0], matrix[i + 1][j][1] - 5, matrix[i + 1][j][2])
            
            glNormal3f(calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[0], calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[1], calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[2])
            glVertex3f(matrix[i + 1][j + 1][0], matrix[i + 1][j + 1][1] - 5, matrix[i + 1][j + 1][2])
            
            glNormal3f(calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[0], calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[1], calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[2])
            glVertex3f(matrix[i][j + 1][0], matrix[i][j + 1][1] - 5, matrix[i][j + 1][2])
            
            glNormal3f(calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[0], calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[1], calculate_normal(matrix[i][j], matrix[i + 1][j], matrix[i + 1][j + 1])[2])
            glVertex3f(matrix[i][j][0], matrix[i][j][1] - 5, matrix[i][j][2])
            
            glNormal3f(calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[0], calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[1], calculate_normal(matrix[i][j], matrix[i + 1][j + 1], matrix[i][j + 1])[2])
            glVertex3f(matrix[i + 1][j + 1][0], matrix[i + 1][j + 1][1] - 5, matrix[i + 1][j + 1][2])
            glEnd()
 

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
        
    random.seed(2)
    matrixValues()    

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()