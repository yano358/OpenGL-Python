import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import random as r
from time import sleep

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)

def shutdown():
    pass

def render(time):
    glClear(GL_COLOR_BUFFER_BIT) #clear memory

    draw_second_fractal(-2.0,-1.5,1,1.5,100,100,100)

    #draw_fractal(-50, -50, 100, 100, 3)

    #draw_triangle_colorful()

    #draw_rect(50,-25,20,20)
    
    glFlush() #flush to memeory

    

def draw_triangle_colorful() -> None:

    glBegin(GL_TRIANGLES)
    glVertex2f(10.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)

    glVertex2f(0.0, 50.0)
    glColor3f(1.0, 0.0, 0.0)

    glVertex2f(50.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)

    glEnd()

def draw_rect(x:int , y:int , width:int , height:int) -> None:

    d: float = r()
    red: float = r()
    green: float = r()
    blue: float = r()
    sleep(0.5)

    glBegin(GL_TRIANGLES)
    glColor3f(red, green, blue)
    glVertex2f(x*d,y*d)

    glColor3f(red, green, blue)
    glVertex2f((x + width)*d, y*d)

    glColor3f(red, green, blue)
    glVertex2f((x + width)*d, (y + height)*d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(red, green, blue)
    glVertex2f(x*d,y*d)

    glColor3f(red, green, blue)
    glVertex2f(x*d, (y + height)*d)

    glColor3f(red, green, blue)
    glVertex2f((x + width)*d, (y + height)*d)
    glEnd()

def draw_rect_from_triangle(x:int , y:int , width:int , height:int) -> None:

    glBegin(GL_TRIANGLES)
    glVertex2f(x,y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x,y)
    glVertex2f(x, y + height)
    glVertex2f(x + width, y + height)
    glEnd()

def draw_fractal(x:int,y:int, width:int, height:int, depth:int) -> None:
    if depth <= 0:
        draw_rect_from_triangle(x,y,width,height)
    else:
        new_width = width/3
        new_height = height/3
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:
                    draw_fractal(x + i * new_width, y + j * new_height, new_width, new_height, depth - 1)

def generate_set(c:complex, max_iter:int) -> int:
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def draw_second_fractal(xmin:float,ymin:float,ymax:float,xmax:float,width:int,height:int,max_iter:int) -> None:
    for x in range(width):
        for y in range(height):
            # Map the pixel coordinates to the complex plane
            real = xmin + (xmax - xmin) * x / (width - 1)
            imag = ymin + (ymax - ymin) * y / (height - 1)

            # Calculate the corresponding value in the Mandelbrot set
            c = complex(real, imag)
            iterations = generate_set(c, max_iter)

            # Set color based on the number of iterations
            color = iterations / max_iter  # You can use this value to define the color
            glColor3f(color, color, color)

            # Draw a point at (x, y) with the calculated color
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "grafikaLab", None, None)
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