
import sys

from numpy import pi, linspace, zeros, random, cross, linalg
from math import cos, sin


from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *




viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0

pix2angle = 1.0
piy2angle = 1.0

left_mouse_button_pressed = 0

mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0



n=20
u = linspace(0, 2*pi, num=n+1)
v = linspace(0, 2*pi, num=n+1)
vectors = zeros((n+1, n+1, 3))

tab = zeros((n+1, n+1, 3))

for i in range(n+1):
    for j in range(n+1):
        tab[i][j][0] = -(2.5+cos(u[i])) * -cos(v[j])
        tab[i][j][1] = (2.5+cos(u[i])) * sin(v[j])
        tab[i][j][2] = sin(u[i])

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMaterialfv(GL_FRONT, GL_AMBIENT, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 20.0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.2, 8.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 10.0, 1.0])
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.001)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass



def render(time):
    global theta, phi
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0,1.0, 0.0)

    

    spin(time * 180 / pi)

    doughnutFromTriangles()
    drawNormalVectors()

    glFlush()


def drawNormalVectors() -> None:
    for i in range(0, n):
        for j in range(0, n):
            glBegin(GL_LINES)
            
            glVertex3f(tab[i][j][0],tab[i][j][1],tab[i][j][2])  # Start of the line is the vertex position
            glVertex3fv(tab[i][j] -0.5* vectors[i][j])  # End of the line is a point in the direction of the normal vector
            glEnd()





def doughnutFromTriangles() -> None:

    for i in range(0,n):
        for j in range(0,n):
            glBegin(GL_TRIANGLES)
            #glNormal3fv(vectors[i][j]*tab[i][j])
            glNormal3fv(tab[i][j] -2.5* vectors[i][j])
            glVertex3fv(tab[i][j])

            #glNormal3fv(vectors[i+1][j]*tab[i+1][j])
            glVertex3fv(tab[i+1][j])
            
            #glNormal3fv(vectors[i][j+1]*tab[i][j+1])
            glVertex3fv(tab[i][j+1])

            #glNormal3fv(vectors[i+1][j]*tab[i+1][j])
            glVertex3fv(tab[i+1][j])
           
            #glNormal3fv(vectors[i+1][j+1]*tab[i+1][j+1])
            glVertex3fv(tab[i+1][j+1])
            
            #glNormal3fv(vectors[i][j+1]*tab[i][j+1])
            glVertex3fv(tab[i][j+1])
            glEnd()

def fillNormalVectors() -> None:
    for i in range(n):
        for j in range(n):
            
            v1 = tab[(i+1)][j] - tab[i][j]
            v2 = tab[i][(j+1)] - tab[i][j]

            
            normal = cross(v1, v2)
            normal = normal / linalg.norm(normal)

            
            vectors[i][j] = normal


def spin(angle) -> None:
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

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

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab5_fin", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)


    random.seed(1)
    fillNormalVectors()

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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

