import sys

from numpy import pi, linspace, ndarray, zeros, random
from math import cos, sin


from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #axes()



    #eggFromPoints(time)
    #eggFromLines(time)
    #doughnutFromTriangles(time)
    doughnutFromTrianglesStrip(time)
    #shapeFromTrianglesStrip(time)

    glFlush()

def eggFromPoints(time) -> None:
    spin(time * 180 / pi)

    n:int = 50
    tab:ndarray = [[[0.0 for _ in range(3)] for _ in range(n)] for _ in range(n)]
    v:ndarray = linspace(0,1,n)
    u:ndarray = linspace(0,1,n)
    for i in range(n):
        for j in range(n):
            tab[i][j][0]=(-90*pow(u[i],5)+225*pow(u[i],4)-270*pow(u[i],3)+180*pow(u[i],2)-45*u[i])*cos(pi*v[j])
            tab[i][j][1]=(160*pow(u[i],4)-320*pow(u[i],3)+160*pow(u[i],2))-5
            tab[i][j][2]=(-90*pow(u[i],5)+225*pow(u[i],4)-270*pow(u[i],3)+180*pow(u[i],2)-45*u[i])*sin(pi*v[j])


    glBegin(GL_POINTS)
    for i in range(n):
        for j in range(n):
            glVertex3fv(tab[i][j])
    glEnd()


def eggFromLines(time) -> None:
    spin(time * 180 / pi)

    n:int = 50
    tab:ndarray = [[[0.0 for _ in range(3)] for _ in range(n)] for _ in range(n)]
    v:ndarray = linspace(0,1,n)
    u:ndarray = linspace(0,1,n)
    for i in range(n):
        for j in range(n):
            tab[i][j][0]=(-90*pow(u[i],5)+225*pow(u[i],4)-270*pow(u[i],3)+180*pow(u[i],2)-45*u[i])*cos(pi*v[j])
            tab[i][j][1]=(160*pow(u[i],4)-320*pow(u[i],3)+160*pow(u[i],2))-5
            tab[i][j][2]=(-90*pow(u[i],5)+225*pow(u[i],4)-270*pow(u[i],3)+180*pow(u[i],2)-45*u[i])*sin(pi*v[j])
    
    glBegin(GL_LINES)
    for i in range(n):
        for j in range(n):
            if(i+1<n):
                glVertex3fv(tab[i][j])
                glVertex3fv(tab[i+1][j])
            if(j+1<n):
                glVertex3fv(tab[i][j])
                glVertex3fv(tab[i][j+1])
    glEnd()


def doughnutFromTriangles(time) -> None:

    glRotatef(time * 180 / pi, 0.0, 1.0, 0.0)
    glRotatef(time * 180 / pi, 1.0, 0.0, 0.0)
    glRotatef(time * 180 / pi, 0.0, 0.0, 1.0)

    n=50
    u = linspace(0, 2*pi, num=n)
    v = linspace(0, 2*pi, num=n)

    tab = zeros((n, n, 3))

    for i in range(n):
        for j in range(n):
            tab[i][j][0] = -(2.5+cos(u[i])) * -cos(v[j])
            tab[i][j][1] = (2.5+cos(u[i])) * sin(v[j])
            tab[i][j][2] = sin(u[i])


    random.seed(2) #constantly random colors (same every time)
    glBegin(GL_TRIANGLES)
    for i in range(n-1):
        for j in range(n-1):
            glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(tab[i][j])
            glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(tab[i+1][j])
            glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(tab[i][j+1])
            
            glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(tab[i+1][j])
            glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(tab[i+1][j+1])
            glColor3f(random.random(),random.random(),random.random())
            glVertex3fv(tab[i][j+1])
    glEnd()

def doughnutFromTrianglesStrip(time) -> None:

    spin(time * 180 / pi)

    n=50
    u = linspace(0, 2*pi, num=n)
    v = linspace(0, 2*pi, num=n)

    tab = zeros((n, n, 3))

    for i in range(n):
        for j in range(n):
            tab[i][j][0] = -(2.5+cos(u[i])) * -cos(v[j])
            tab[i][j][1] = (2.5+cos(u[i])) * sin(v[j])
            tab[i][j][2] = sin(u[i])

    
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(n-1):
        for j in range(n):
            glColor3f(1,1,0)
            glVertex3fv(tab[i][j])
            glColor3f(0,1,1)
            glVertex3fv(tab[i+1][j])
    glEnd()

def shapeFromTrianglesStrip(time) -> None:
    spin(time * 180 / pi)

    n=50
    u = linspace(0, 1, num=n)
    v = linspace(0, 1, num=n)

    tab = zeros((n, n, 3))

    for i in range(n):
        for j in range(n):
            tab[i][j][0] = weierstrass_function(u[i])
            tab[i][j][1] = weierstrass_function(v[j])
            tab[i][j][2] = weierstrass_function(u[i] + v[j])

    
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(n-1):
        for j in range(n):
            glColor3f(1,1,0)
            glVertex3fv(tab[i][j])
            glColor3f(0,1,1)
            glVertex3fv(tab[i+1][j])
    glEnd()

def weierstrass_function(x):
    #params
    a = 0.7
    b = 5
    num_terms = 50

    result = 0
    for n in range(num_terms):
        result += (a**n) * cos(b**n * pi * x)

    return result

def spin(angle) -> None:
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab3", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

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