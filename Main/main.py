#================================ASPECTOS_TECNICOS==============================
from pygame.locals import *
import pygame as pg
from copy import deepcopy
from copy import copy
import numpy.linalg as linalg
import numpy as np
import math as mt


clock = pg.time.Clock()
FPS = 30

pg.init()

# dimenciones
display_width =  920
display_height = 920

win = pg.display.set_mode((display_width,display_height),FULLSCREEN)
pg.display.set_caption("Proyeccion de Pespectiva",)

transparent = (0,0,0,0)
white = (255,255,255, 155)
black = (0,0,0, 255)

light_pink = (255, 173, 173)
deep_champagne = (255, 214, 165)
lemon_yellow = (253, 255, 182)
tea_green = (202, 255, 191)
celeste = (155, 246, 255)
mauve = (255, 198, 255)
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

def General():

    a = 0.0
    b = 1.0/(10.0**0.5)
    c = -3.0/(10.0**0.5)
    q = 2*(10.0**0.5)
    z = 800.0

    a0 = 1.0
    a2 = -a/c
    a3 = (z*a)/c
    b1 = 1.0
    b2 = -b/c
    b3 = (z*b)/c
    c2 = -z/(q*c)
    c3 = (z**2)/(q*c)+z
    d2 = -1.0/(q*c)
    d3 = z/(q*c)+1.0
                        #  0 1 2 3
    matGen = np.matrix([[a0,0,a2,a3],  #A
                         [0,b1,b2,b3],  #B
                         [0,0,c2,c3],   #C
                         [0,0,d2,d3]])  #D
    return matGen


#Proyection Matrix
def Proj ():
    # Distancias de planos de distorsión
    Near = 1
    Far = 5000.0
    Fov = 45.0
    AspectRatio = display_height / display_width
    FovRad = 1.0 / mt.tan(mt.radians(Fov) * 0.5 )

    a0 = FovRad # * AspectRatio
    b1 = FovRad
    c2 = (Far+Near) / (Far - Near)
    d2 = (2*Far * Near) / (Far - Near)
    c3 = -1.0
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


# Rotation y
def Roty (theta:float):

    a0 = mt.cos(mt.radians(theta))
    a2 = mt.sin(mt.radians(theta))
    b1 = 1.0
    c0 = -(mt.sin(mt.radians(theta)))
    c2 = mt.cos(mt.radians(theta))
    d3 = 1.0
                        #  0 1 2 3
    matRoty = np.matrix([[a0,0,a2,0],   #A
                         [0,b1,0,0],    #B
                         [c0,0,c2,0],   #C
                         [0,0,0,d3]])   #D
    return matRoty

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
    return sclMov


def cuadradoide(mesh_Cube:list,thetaX:float,thetaZ:float,thetaY:float,Color:int):
    for tri in mesh_Cube:
        cameraV = np.array([0.0,0.0,0.0,0.0])
        projected = []
        rotatedZ = []
        rotatedXZ = []
        rotatedXZY = []

        for vec in tri:
            # Rot in z axis
            temp = MultMatrix4X4Vector1x4(vec,Rotz(thetaZ))
            rotatedZ.append(temp)

        for vec in rotatedZ:
            # Rot in z axis
            temp = MultMatrix4X4Vector1x4(vec,Rotx(thetaX))
            rotatedXZ.append(temp)

        for vec in rotatedXZ:
            # Rot in y axis
            temp = MultMatrix4X4Vector1x4(vec,Roty(thetaY))
            rotatedXZY.append(temp)

        translated = deepcopy(rotatedXZY)
        # Alejar la camara
        translated[0][2] = rotatedXZY[0][2] + 3.0
        translated[1][2] = rotatedXZY[1][2] + 3.0
        translated[2][2] = rotatedXZY[2][2] + 3.0

        # ===========| CAMPO DE VISIÓN |=========== #
        # cameraLine
        cl0 =  translated[0][0] - cameraV[0]
        cl1 =  translated[0][1] - cameraV[1]
        cl2 =  translated[0][2] - cameraV[2]


        #Normal de cada triangulo
        L1a = translated[1][0] - translated[0][0]
        L1b = translated[1][1] - translated[0][1]
        L1c = translated[1][2] - translated[0][2]

        L2a = translated[2][0] - translated[0][0]
        L2b = translated[2][1] - translated[0][1]
        L2c = translated[2][2] - translated[0][2]

        Line1 = np.array([L1a,L1b,L1c])
        Line2 = np.array([L2a,L2b,L2c])

        normal = np.cross(Line1,Line2)

        # Normalizando la normal (jejeje suena raro)
        normL = mt.sqrt((normal[0]**2)+(normal[1]**2)+(normal[2]**2))
        normal[0] = normal[0]/ normL
        normal[1] = normal[1]/ normL
        normal[2] = normal[2]/ normL


        if ((normal[0]*cl0)+(normal[1]*cl1)+(normal[2]*cl2)) > 0:
            # Proyection 3D-->2D
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
            x0 += 3.5
            y0 += 3.5
            x1 += 3.5
            y1 += 3.5
            x2 += 3.5
            y2 += 3.5

            x0 *= (0.15*display_width)
            y0 *= (0.15*display_height)
            x1 *= (0.15*display_width)
            y1 *= (0.15*display_height)
            x2 *= (0.15*display_width)
            y2 *= (0.15*display_height)
            # ============================================ #
            thic = 0
            thic2 = 5
            COL = [light_pink,deep_champagne,lemon_yellow,tea_green,celeste,mauve]
            pg.draw.polygon(win,COL[Color],[(x0,y0),(x1,y1),(x2,y2)],thic)
            pg.draw.polygon(win,white,[(x0,y0),(x1,y1),(x2,y2)],thic2)

def ProyeccionText(x:float,y:float,Color:int):
    font1 = pg.font.SysFont("DM Mono",55,False,False,None) #Para mejor experiencia instala hay que intalar la tipografía que está en la carpeta.
    COL = [lemon_yellow,tea_green,deep_champagne,light_pink,celeste,mauve]
    text = font1.render("Proyección de Perspectiva",True, COL[Color]) # Render del texto en la pantalla
    text2 = font1.render("Proyección de Perspectiva",True, (255,255,255)) # Render del texto en la pantalla
    win.blit(text2,(x/17,(4*y/5)))
    win.blit(text,(x/17,(4*y/5)+5))


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
e9 = np.array([0.0,1.0,0.0,1.0])


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

# Piram other faces
t13 = [e1,e9,e4]
t14 = [e4,e9,e8]
t15 = [e8,e9,e5]
t16 = [e5,e9,e1]


mesh_Cube = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12]
mesh_Piram = [t11,t12,t13,t14,t15,t16]
# mesh_Cube = [t1,t2,t5,t6]
# #===============================================================================
#
def main(mesh):
    thetaX = 0.0
    thetaZ = 0.0
    thetaY = 0.0

    Color = 0

    # b_ms = pg.mixer
    # b_ms.music.load("Flume.mp3")
    # b_ms.music.play(-1)


    while True:
        win.fill(black)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()


        pressed_keys = pg.key.get_pressed()

        if pressed_keys[K_q]:
            thetaX += 1.5
        elif pressed_keys[K_a]:
            thetaX -= 1.5

        if pressed_keys[K_w]:
            thetaZ += 1.5
        elif pressed_keys[K_s]:
            thetaZ -= 1.5

        if pressed_keys[K_e]:
            thetaY += 1.5
        elif pressed_keys[K_d]:
            thetaY -= 1.5

        if pressed_keys[K_r]:
            thetaX += 1.5
            thetaY += 1.5
            thetaZ += 1.5

        elif pressed_keys[K_f]:
            thetaX -= 1.5
            thetaY -= 1.5
            thetaZ -= 1.5

        if pressed_keys[K_m]:
            thetaX = 0
            thetaY = 0
            thetaZ = 0

        if pressed_keys[K_z]:
            pg.quit()
            quit()

        if pressed_keys[K_c]:
            if (Color < 5):
                Color += 1
            else:
                Color = 0

        ProyeccionText(display_width,display_height+100,Color)
        ProyeccionText(display_width,display_height-0,Color)
        ProyeccionText(display_width,display_height-100,Color)
        ProyeccionText(display_width,display_height-200,Color)
        ProyeccionText(display_width,display_height-300,Color)
        ProyeccionText(display_width,display_height-400,Color)
        ProyeccionText(display_width,display_height-500,Color)
        ProyeccionText(display_width,display_height-600,Color)
        ProyeccionText(display_width,display_height-700,Color)
        ProyeccionText(display_width,display_height-800,Color)
        ProyeccionText(display_width,display_height-900,Color)

        cuadradoide(mesh,thetaX,thetaZ,thetaY,Color)


        pg.display.update()


        clock.tick(FPS)


#
# # ==============================================================================

main(mesh_Cube)
# main(mesh_Piram)
