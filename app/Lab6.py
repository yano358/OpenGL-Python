import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

from numpy import zeros
from math import cos, sin, pi

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

a_key = 1
texture_change_key_s = 0
texture_change_key_d = 0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.95, 0.95, 0.95, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

texture1 = Image.open("app\\cat.tga")
texture2 = Image.open("app\\tekstura.tga")
texture_egg = Image.open("app\\znanyprowadzocy1.tga")
texture_egg2 = Image.open("app\\znanyprowadzocy2.tga")

n = 20
matrix = zeros((n + 1, n + 1, 3))
matrix_vectors = zeros((n + 1, n + 1, 3))
matrix_textures = zeros((n + 1, n + 1, 2))

def startup():
    global texture1, texture2

    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    #texture1 = Image.open("app\\cat.tga")
    #texture2 = Image.open("app\\tekstura.tga")

    #glTexImage2D(
    #    GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
    #    GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    #)

def starting_triangle():
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0.0, 5.0, 0.0)
    glEnd()

def textured_square():
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)
    glEnd()

def pyramid_1(mode:bool):
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)

    if mode:
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-5.0, -5.0, 0.0)

    glEnd()

def pyramid_2(mode:bool):
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 5.0, 0.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, 0.0, -5.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 0.0, 5.0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 0.0, 5.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, 0.0, -5.0)

    if mode:
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-5.0, 0.0, -5.0)

    glEnd()



def eggTriangle():
    for i in range(0, n):
        for j in range (0,n):
            if (i>(0.5*n)):
                glFrontFace(GL_CW)
            else:
                glFrontFace(GL_CCW)

            glBegin(GL_TRIANGLES)
            glTexCoord2f(matrix_textures[i][j][0], matrix_textures[i][j][1])
            glNormal3f(matrix_vectors[i][j+1][0], matrix_vectors[i][j+1][1], matrix_vectors[i][j+1][2])
            glVertex3f(matrix[i][j+1][0], matrix[i][j+1][1]-5, matrix[i][j+1][2])

            glTexCoord2f(matrix_textures[i][j][0], matrix_textures[i][j][1])
            glNormal3f(matrix_vectors[i][j][0], matrix_vectors[i][j][1], matrix_vectors[i][j][2])
            glVertex3f(matrix[i][j][0], matrix[i][j][1]-5, matrix[i][j][2])

            glTexCoord2f(matrix_textures[i+1][j+1][0], matrix_textures[i+1][j+1][1])
            glNormal3f(matrix_vectors[i+1][j+1][0], matrix_vectors[i+1][j+1][1], matrix_vectors[i+1][j+1][2])
            glVertex3f(matrix[i+1][j+1][0], matrix[i+1][j+1][1]-5, matrix[i+1][j+1][2])

            glEnd()

            glBegin(GL_TRIANGLES)
            glTexCoord2f(matrix_textures[i][j][0], matrix_textures[i][j][1])
            glNormal3f(matrix_vectors[i][j][0], matrix_vectors[i][j][1], matrix_vectors[i][j][2])
            glVertex3f(matrix[i][j][0], matrix[i][j][1]-5, matrix[i][j][2])

            glTexCoord2f(matrix_textures[i+1][j][0], matrix_textures[i+1][j][1])
            glNormal3f(matrix_vectors[i+1][j][0], matrix_vectors[i+1][j][1], matrix_vectors[i+1][j][2])
            glVertex3f(matrix[i+1][j][0], matrix[i+1][j][1]-5, matrix[i+1][j][2])

            glTexCoord2f(matrix_textures[i+1][j+1][0], matrix_textures[i+1][j+1][1])
            glNormal3f(matrix_vectors[i+1][j+1][0], matrix_vectors[i+1][j+1][1], matrix_vectors[i+1][j+1][2])
            glVertex3f(matrix[i+1][j+1][0], matrix[i+1][j+1][1]-5, matrix[i+1][j+1][2])

            glEnd()

def fill_matrix_textures():
    for i in range(0, n + 1):
        for j in range(0, n + 1):
            u = i / n
            v = j / n

            if(i>(0.5*n)):
                matrix_textures[i][j][0] = v
                matrix_textures[i][j][1] = 1 - u*2
            else:
                matrix_textures[i][j][0] = v
                matrix_textures[i][j][1] = u*2

def fill_matrix_egg():
    for i in range(0, n+1):
        for j in range(0, n+1):
            u = i / n
            v = j / n

            matrix[i][j][0] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * cos(pi * v)
            matrix[i][j][1] = 160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2)
            matrix[i][j][2] = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * sin(pi * v)

def fill_matrix_normals():
    for i in range(0, n+1):
        for j in range(0, n+1):
            u = i / n
            v = j / n

            x_u = (-450*pow(u,4) + 900*pow(u,3) - 810*pow(u,2) + 360*u - 45)*cos(pi*v)
            x_v = pi * (90*pow(u,5) - 225*pow(u,4) + 270*pow(u,3) - 180*pow(u,2) + 45*u)*sin(pi*v)

            y_u = 640*pow(u,3) - 960*pow(u,2) + 320*u
            y_v = 0

            z_u = (-450*pow(u,4) + 900*pow(u,3) - 810*pow(u,2) + 360*u - 45)*sin(pi*v)
            z_v = (-pi) * (90*pow(u,5) - 225*pow(u,4) + 270*pow(u,3) - 180*pow(u,2) + 45*u)*cos(pi*v)

            x = y_u*z_v - z_u*y_v
            y = z_u*x_v - x_u*z_v
            z = x_u*y_v - y_u*x_v

            sum_vec = pow(x,2) + pow(y,2) + pow(z,2)
            length_vec = pow(sum_vec,0.5)

            if length_vec >0:
                x = x/length_vec
                y = y/length_vec
                z = z/length_vec

            if i>n/2:
                x *= -1
                y *= -1
                z *= -1

            matrix_vectors[i][j][0] = x
            matrix_vectors[i][j][1] = y
            matrix_vectors[i][j][2] = z


def shutdown():
    pass

def render(time):
    global theta, phi,texture1,texture2,a_key,texture_change_key_d


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(phi, 1.0, 0.0, 0.0)
    glRotatef(theta, 0.0, 1.0, 0.0)

    #starting_triangle()
    #pyramid_2(texture_change_key_s)

    #textured_square()
    #pyramid_1(texture_change_key_s)

    eggTriangle()

    if a_key:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, texture1.size[0], texture1.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, texture1.tobytes("raw", "RGB", 0, -1)
        )
    else:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, texture2.size[0], texture2.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, texture2.tobytes("raw", "RGB", 0, -1)
        )

    
    #if texture_change_key_d:
    #    glTexImage2D(
    #        GL_TEXTURE_2D, 0, 3, texture_egg.size[0], texture_egg.size[1], 0,
    #        GL_RGB, GL_UNSIGNED_BYTE, texture_egg.tobytes("raw", "RGB", 0, -1)
    #    )
    #else:
    #    glTexImage2D(
    #        GL_TEXTURE_2D, 0, 3, texture_egg2.size[0], texture_egg2.size[1], 0,
    #        GL_RGB, GL_UNSIGNED_BYTE, texture_egg2.tobytes("raw", "RGB", 0, -1)
    #    )

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
    global a_key,texture_change_key_s,texture_change_key_d

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_A and action == GLFW_PRESS:
        a_key = not a_key

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        texture_change_key_s = not texture_change_key_s

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        texture_change_key_d = not texture_change_key_d


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x,mouse_x_pos_old,delta_y,mouse_y_pos_old

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

    window = glfwCreateWindow(400, 400, "Lab6", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    fill_matrix_normals()
    fill_matrix_egg()
    fill_matrix_textures()

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