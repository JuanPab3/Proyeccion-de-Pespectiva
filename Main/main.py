#================================ASPECTOS_TECNICOS==============================
from pygame.locals import *
import pygame as pg
from copy import deepcopy
from copy import copy
import numpy as np
import math as mt


clock = pg.time.Clock()
FPS = 30

pg.init()

# dimenciones
display_width =  1720
display_height = 920

win = pg.display.set_mode((display_width,display_height))
pg.display.set_caption("Proyeccion de Pespectiva",)

transparent = (0,0,0,0)
white = (255,255,255, 155)
black = (0,0,0, 255)

light_pink = (255, 173, 173, 128)
deep_champagne = (255, 214, 165, 128)
lemon_yellow = (253, 255, 182, 128)
tea_green = (202, 255, 191, 128)
celeste = (155, 246, 255, 128)
mauve = (255, 198, 255, 128)

#=====================================CLASES====================================


#====================================FUNCIONES==================================

def MultMatrix4X4Vector1x4(i:np.array,m:np.matrix):

    temp_mat = i*m

    final_array = np.squeeze(np.asarray(temp_mat))

    if (final_array[3] != 0):
        final_array[0] /= final_array[3]
        final_array[1] /= final_array[3]
        final_array[2] /= final_array[3]

    return final_array



#===============================PROYECTION_MATRIX===============================

#Proyection Matrix
def Proj ():
    # Distancias de planos de distorsión
    Near = 1
    Far = 500.0
    Fov = 45.0
    AspectRatio = display_height / display_width
    FovRad = 1.0 / mt.tan(mt.radians(Fov) * 0.5 )

    a0 = FovRad # * AspectRatio
    b1 = FovRad
    c2 = (Far+Near) / (Far - Near)
    d2 = (2*Far * Near) / (Far - Near)
    c3 = 1.0
                        #  0 1 2 3
    matProj = np.matrix([[a0,0,0,0],    #A
                         [0,b1,0,0],    #B
                         [0,0,c2,c3],   #C
                         [0,0,d2,0]])   #D
    return matProj

# Rotation z
def Rotz (theta:float):

    a0 = mt.cos(mt.radians(theta))
    a1 = mt.sin(mt.radians(theta))
    b0 = -(mt.sin(mt.radians(theta)))
    b1 = mt.cos(mt.radians(theta))
    c2 = 1.0
    d3 = 1.0
                        #  0 1 2 3
    matRotz = np.matrix([[a0,a1,0,0],   #A
                         [b0,b1,0,0],   #B
                         [0,0,c2,0],    #C
                         [0,0,0,d3]])   #D

    return matRotz


# Rotation x
def Rotx (theta:float):

    a0 = 1.0
    b1 = mt.cos(mt.radians(theta))
    b2 = mt.sin(mt.radians(theta))
    c1 = -(mt.sin(mt.radians(theta)))
    c2 = mt.cos(mt.radians(theta))
    d3 = 1.0
                        #  0 1 2 3
    matRotx = np.matrix([[a0,0,0,0],    #A
                         [0,b1,b2,0],   #B
                         [0,c1,c2,0],   #C
                         [0,0,0,d3]])   #D

    return matRotx

# Move xyz;
def mov_xyz(x=0,y=0,z=0):
                        #  0 1 2 3
    matMov = np.matrix([[1,0,0,0],   #A
                        [0,1,1,0],   #B
                        [0,1,1,0],   #C
                        [x,y,z,1]])  #D

    return matMov

def scale_xyz(x=1,y=1,z=1):
                        #  0 1 2 3
    sclMov = np.matrix([[x,0,0,0],   #A
                        [0,y,0,0],   #B
                        [0,0,z,0],   #C
                        [0,0,0,1]])  #D


def cuadradoide(mesh_Cube:list,thetaX:float,thetaZ:float):
    for tri in mesh_Cube:
        projected = []
        rotatedZ = []
        rotatedXZ = []


        for vec in tri:
            # Efecto de proyección
            temp = MultMatrix4X4Vector1x4(vec,Rotz(thetaZ))
            rotatedZ.append(temp)

        for vec in rotatedZ:
            temp = MultMatrix4X4Vector1x4(vec,Rotx(thetaX))
            rotatedXZ.append(temp)


        translated = deepcopy(rotatedXZ)
        # Alejar la camara
        translated[0][2] = rotatedXZ[0][2] + 3.0
        translated[1][2] = rotatedXZ[1][2] + 3.0
        translated[2][2] = rotatedXZ[2][2] + 3.0

        # print(translated)

        for vec in translated:
            # Efecto de proyección
            temp = MultMatrix4X4Vector1x4(vec,Proj())
            projected.append(temp);

        x0 = projected[0][0]
        y0 = projected[0][1]
        x1 = projected[1][0]
        y1 = projected[1][1]
        x2 = projected[2][0]
        y2 = projected[2][1]

        # ===========| ESCALAR TRIANGULOS |=========== #
        x0 += 4.0
        y0 += 4.0
        x1 += 4.0
        y1 += 4.0
        x2 += 4.0
        y2 += 4.0

        x0 *= (0.1*display_width)
        y0 *= (0.1*display_height)
        x1 *= (0.1*display_width)
        y1 *= (0.1*display_height)
        x2 *= (0.1*display_width)
        y2 *= (0.1*display_height)
        # ============================================ #

        pg.draw.polygon(win,deep_champagne,[(x0,y0),(x1,y1),(x2,y2)],1)






#=================================CUBE_PARAMETERS===============================
#
# Esquinas del Cubo
#                x    y   z   w
e1 = np.array([-1.0,-1.0,1.0,1.0])
e2 = np.array([-1.0,1.0,1.0,1.0])
e3 = np.array([1.0,1.0,1.0,1.0])
e4 = np.array([1.0,-1.0,1.0,1.0])
e5 = np.array([-1.0,-1.0,-1.0,1.0])
e6 = np.array([-1.0,1.0,-1.0,1.0])
e7 = np.array([1.0,1.0,-1.0,1.0])
e8 = np.array([1.0,-1.0,-1.0,1.0])

#
# e1 = np.array([0.0,0.0,0.0,1.0])
# e2 = np.array([0.0,1.0,0.0,1.0])
# e3 = np.array([1.0,1.0,0.0,1.0])
# e4 = np.array([1.0,0.0,0.0,1.0])
# e5 = np.array([0.0,0.0,1.0,1.0])
# e6 = np.array([0.0,1.0,1.0,1.0])
# e7 = np.array([1.0,1.0,1.0,1.0])
# e8 = np.array([1.0,0.0,1.0,1.0])



# Front face triangles
t1 = [e1,e2,e3]
t2 = [e1,e3,e4]

# Right face triangles
t3 = [e4,e3,e7]
t4 = [e4,e7,e8]

# Back face triangles
t5 = [e8,e7,e6]
t6 = [e8,e6,e5]

# Left face triangles
t7 = [e5,e6,e2]
t8 = [e5,e2,e1]

# Top face triangles
t9 = [e2,e6,e7]
t10 = [e2,e7,e3]

# Bottom face triangles
t11 = [e8,e5,e1]
t12 = [e8,e1,e4]


mesh_Cube = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12]
# mesh_Cube = [t1,t2,t5,t6]
# #===============================================================================
#
def main(mesh):
    thetaX = 1
    thetaZ = 1
    while True:
        win.fill(black)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()


        pressed_keys = pg.key.get_pressed()

        if pressed_keys[K_q]:
            thetaX += 1
        elif pressed_keys[K_a]:
            thetaX -= 1

        if pressed_keys[K_w]:
            thetaZ += 1
        elif pressed_keys[K_s]:
            thetaZ -= 1

        if pressed_keys[K_e]:
            thetaX += 1
            thetaZ += 1

        elif pressed_keys[K_d]:
            thetaX -= 1
            thetaZ -= 1


        cuadradoide(mesh,thetaX,thetaZ)




        pg.display.update()


        clock.tick(FPS)


main(mesh_Cube)
#
# # ==============================================================================
