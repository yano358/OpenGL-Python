#done for 4.0 -> 4.5 and 5.0 are in next file
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, pi


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi:float = 0.0
pix2angle = 1.0
piy2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
radius:float=5.0


#colors of material
mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
#shining
mat_shininess = 20.0

#colors of light source 0
light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

#colors of light source 1
light_list=[
[0.0, 0.0, 1.0, 1.0], #ambient1
[1.0, 0.0, 0.0, 1.0], #diffuse1
[0.0, 1.0, 0.0, 1.0] #specular1
]
#position of light source 1
light_position1 = [0.0, 10.0, 0.0, 1.0]

names_to_display:dict = {
    0: "First component",
    1: "Second component",
    2: "Third component",
    3: "Fourth component"
}
#loss of light
att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001
#key input
up:float=0
down:float=1
n:bool=0
next_component:int=0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    #display light0
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    #display light1
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_list[0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_list[1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_list[2])
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)


    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def render(time):
    global theta, phi, light_position1, radius

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * piy2angle

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3,10,10)
    gluDeleteQuadric(quadric)
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    x_light=radius*cos(2*pi*theta/360)*cos(2*pi*phi/360)
    y_light=radius*sin(2*pi*phi/360)
    z_light=radius*sin(2*pi*theta/360)*cos(2*pi*phi/360)
    glTranslate(x_light,y_light,z_light)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5,6,5)
    gluDeleteQuadric(quadric)

    light_position1=[x_light,y_light,z_light,1.0]
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    glFlush()

def shutdown():
    pass

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
    global up,down,n,next_component
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        light_list[next_component][n]+=0.1
        light_list[next_component][n]=light_list[next_component][n]%1
    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        light_list[next_component][n]-=0.1
        light_list[next_component][n]=light_list[next_component][n]%1
    if key == GLFW_KEY_N and action == GLFW_PRESS:
        n+=1
        n=n%3
        print("Current component: "+str(n))
    if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
        next_component+=1
        next_component=next_component%3
        print("Selected vector: "+names_to_display[next_component])


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
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "Lab5", None, None)
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
        startup() #using startup instead of render im too lazy to change it
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()