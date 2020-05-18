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

def MultiplyMatrixVector(i:np.array,m:np.ndarray,v:int):
    temp_array = np.zeros((1,4))


    temp_array[0][0] = float(i[v][0]*m[0][0]) + float(i[v][1]*m[0][1]) + float(i[v][2]*m[0][2]) + float(m[0][3])
    temp_array[0][1] = float(i[v][0]*m[1][0]) + float(i[v][1]*m[1][1]) + float(i[v][2]*m[1][2]) + float(m[1][3])
    temp_array[0][2] = float(i[v][0]*m[2][0]) + float(i[v][1]*m[2][1]) + float(i[v][2]*m[2][2]) + float(m[2][3])
    temp_array[0][3] = float(i[v][0]*m[3][0]) + float(i[v][1]*m[3][1]) + float(i[v][2]*m[3][2]) + float(m[3][3])

    # print(i[0][0])



    o = np.array([temp_array[0][0],temp_array[0][1],temp_array[0][2]])
    # w distinto de cero?
    if (temp_array[0][3] != 0):
        x = temp_array[0][0] / temp_array[0][3]
        y = temp_array[0][1] / temp_array[0][3]
        z = temp_array[0][2] / temp_array[0][3]
        o = np.array([x,y,z])

    return o



#===============================PROYECTION_MATRIX===============================

#Proyection Matrix
matProj = np.zeros((4,4))


# Distancias de planos de distorsión
Near = 1;
Far = 500.0;
Fov = 45.0;
AspectRatio = display_height / display_width;
FovRad = 1.0 / mt.tan(mt.radians(Fov) * 0.5 );

matProj[0][0] =  FovRad # * AspectRatio
matProj[1][1] = FovRad
matProj[2][2] = (Far+Near) / (Far - Near)
matProj[3][2] = (2*Far * Near) / (Far - Near)
matProj[2][3] = 1.0;
matProj[3][3] = 0.0;

# Rotation z
def Rotz (theta:float):
    matRotz = np.zeros((4,4))

    matRotz[0][0] = mt.cos(mt.radians(theta))
    matRotz[0][1] = mt.sin(mt.radians(theta))
    matRotz[1][0] = -(mt.sin(mt.radians(theta)))
    matRotz[1][1] = mt.cos(mt.radians(theta))
    matRotz[2][2] = 1.0
    matRotz[3][3] = 1.0

    return matRotz




# Rotation x
def Rotx (theta:float):
    matRotx = np.zeros((4,4))

    matRotx[0][0] = 1.0
    matRotx[1][1] = mt.cos(mt.radians(theta))
    matRotx[1][2] = mt.sin(mt.radians(theta))
    matRotx[2][1] = -(mt.sin(mt.radians(theta)))
    matRotx[2][2] = mt.cos(mt.radians(theta))
    matRotx[3][3] = 1.0

    return matRotx



def cube(mesh_Cube:list,thetaX:float,thetaZ:float):
    for t in mesh_Cube:
        proyeccion = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0])]

        rotateZ = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0])]
        rotateZX = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0]),np.array([0.0,0.0,0.0])]

        rotateZ[0] = MultiplyMatrixVector(t,Rotz(thetaZ),0)
        rotateZ[1] = MultiplyMatrixVector(t,Rotz(thetaZ),0)
        rotateZ[2] = MultiplyMatrixVector(t,Rotz(thetaZ),0)

        rotateZX[0] = MultiplyMatrixVector(rotateZ,Rotx(thetaX),0)
        rotateZX[1] = MultiplyMatrixVector(rotateZ,Rotx(thetaX),0)
        rotateZX[2] = MultiplyMatrixVector(rotateZ,Rotx(thetaX),0)

        translated = deepcopy(rotateZX)
        for v in range(len(translated)):
            translated[v][2] = rotateZX[v][2]+3

        proyeccion[0] = MultiplyMatrixVector(translated,matProj,0)
        proyeccion[1] = MultiplyMatrixVector(translated,matProj,1)
        proyeccion[2] = MultiplyMatrixVector(translated,matProj,2)

        proyeccion[0][0] += 1.0
        proyeccion[0][1] += 1.0
        proyeccion[1][0] += 1.0
        proyeccion[1][1] += 1.0
        proyeccion[2][0] += 1.0
        proyeccion[2][1] += 1.0

        proyeccion[0][0] *= (0.5*display_width)
        proyeccion[0][1] *= (0.5*display_height)
        proyeccion[1][0] *= (0.5*display_width)
        proyeccion[1][1] *= (0.5*display_height)
        proyeccion[2][0] *= (0.5*display_width)
        proyeccion[2][1] *= (0.5*display_height)

        thic = 1
        # pg.draw.line(win,celeste,(proyeccion[0][0], proyeccion[0][1]),(proyeccion[1][0], proyeccion[1][1]),thic)
        # pg.draw.line(win,celeste,(proyeccion[1][0], proyeccion[1][1]),(proyeccion[2][0], proyeccion[2][1]),thic)
        # pg.draw.line(win,celeste,(proyeccion[2][0], proyeccion[2][1]),(proyeccion[1][0], proyeccion[1][1]),thic)
        pg.draw.polygon(win,tea_green,[(proyeccion[0][0], proyeccion[0][1]),(proyeccion[1][0], proyeccion[1][1]),(proyeccion[2][0], proyeccion[2][1])],thic)




#=================================CUBE_PARAMETERS===============================

# Esquinas del Cubo
#               x   y   z
e1 = np.array([0.0,0.0,0.0])
e2 = np.array([0.0,1.0,0.0])
e3 = np.array([1.0,1.0,0.0])
e4 = np.array([1.0,0.0,0.0])
e5 = np.array([0.0,0.0,1.0])
e6 = np.array([0.0,1.0,1.0])
e7 = np.array([1.0,1.0,1.0])
e8 = np.array([1.0,0.0,1.0])


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
#===============================================================================

def main(mesh):
    thetaX = 1
    thetaZ = 1
    while True:
        # win.fill(black)

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
        #
        # if pressed_keys[K_e]:
        # elif pressed_keys[K_d]:


        cube(mesh,thetaX,thetaZ)




        pg.display.update()


        clock.tick(FPS)


main(mesh_Cube)

# ==============================================================================
