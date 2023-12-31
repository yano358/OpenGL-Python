import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import pi, sin, cos

viewer = [0.0, 0.0, 10.0]


theta = 180.0
pix2angle = 1.0
piy2angle = 1.0
piz2angle = 1.0
scale:float = 1.0
R=15.0

left_mouse_button_pressed:bool = 0
right_mouse_button_pressed:bool = 0
a_key_pressed:bool = 0
s_key_pressed:bool = 0


mouse_x_pos_old = 0
mouse_y_pos_old:float = 0

delta_x = 0
delta_y:float = 0.0
delta_z:float = 0.0



phi:float = 0.0
zeta:float = 0.0

radius:float = 5.0

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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

revert:float = 1.0
def render(time):
    global theta, phi, scale, revert, radius

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #gluLookAt(viewer[0], viewer[1], viewer[2],
    #          0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, revert, 0.0)
    

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle
    #glRotatef(theta, 0.0, 1.0, 0.0)
    #glRotatef(phi, 1.0, 0.0, 0.0)

    if a_key_pressed:
        scale+=delta_x*0.01
    if scale>=1.5:
        scale=1.49
    glScalef(scale,scale,scale)

    if s_key_pressed and scale<1.5 and scale>0.5:
        scale-=delta_x*0.01
    if scale<=0.5:
        scale=0.51
    glScalef(scale,scale,scale)

    if right_mouse_button_pressed:
        if delta_x>0 and radius<10:
            radius+=1
        elif radius>=1:
            radius-=1

    viewer[0] = radius *cos(theta * 2*pi / 360) * cos(2*phi * pi / 360)
    viewer[1] = radius *sin(phi * pi*2 / 360)
    viewer[2] = radius *sin(theta * pi *2/ 360) * cos(phi * pi *2/ 360)

    
    if phi>180:
        phi-=360 
    elif phi<=-180:
        phi+=360

    if phi<-90 or phi>90:
        revert=-1.0
    else:
        revert=1.0

    axes()
    example_object()

    glFlush()


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
    global a_key_pressed
    global s_key_pressed
    global left_mouse_button_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        a_key_pressed = 1
    else:
        a_key_pressed = 0

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        s_key_pressed = 1
    else:
        s_key_pressed = 0

    if key==GLFW_KEY_M and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0



def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab 4", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

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