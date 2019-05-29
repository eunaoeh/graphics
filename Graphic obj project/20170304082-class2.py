import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os
np.seterr(divide='ignore', invalid='ignore')

Azimuth = np.radians(60)
Elevation = np.radians(45)
r = 4
eye_x= r*np.cos(Elevation)*np.sin(Azimuth)
eye_y= r*np.sin(Elevation)
eye_z= r*np.cos(Elevation)*np.cos(Azimuth)
at_x = 0
at_y = 0
at_z = 0
up_x = 0
up_y = 1
up_z = 0
isDrag = 0
u=np.array([0.,0.,0.])
v=np.array([0.,0.,0.])
w=np.array([0.,0.,0.])
x=0
y=0
z=0
vertex = []
normal = []
index = []
arr = []


def render():
    global eye_x,eye_y,eye_z, at_x, at_y, at_z, up_x, up_y, up_z
    global Elevation, Azimuth, r, x, y, z
    global gVertexArrayIndexed, gIndexArray, isAvg
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.01, 300)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if np.cos(Elevation) < 0:
        up_y = -1
    else:
        up_y = 1

    eye_y = r*np.sin(Elevation) + at_x
    eye_z = r*np.cos(Elevation)*np.cos(Azimuth) + at_y
    eye_x = r*np.cos(Elevation)*np.sin(Azimuth) + at_z

    gluLookAt(eye_x-x, eye_y-y, eye_z-z,
              at_x-x, at_y-y, at_z-z, up_x, up_y, up_z)
    
    r = np.sqrt(np.square(eye_x-at_x)+np.square(eye_y-at_y)+np.square(eye_z-at_z))

    drawFrame()
    
    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glEnable(GL_RESCALE_NORMAL)
    
    # light position
    glPushMatrix()

    glLightfv(GL_LIGHT0, GL_POSITION, (3.,3.,3.,0.))
    glPopMatrix()

    # light intensity for each color channel
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.0001,.0001,.0001,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    glPushMatrix()
    glLightfv(GL_LIGHT1, GL_POSITION, (-3., -3., -3., 1.))
    glPopMatrix()
    
    # light intensity for each color channel
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.001,.001,.001,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

    # material reflectance for each color channel
    objectColor = (0.95,0.78,0.,1.)
    specularObjectColor = (.8,.8,.8,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    
    if isAvg == 0:
        drawCube_glDrawElements()
    elif isAvg == 1:
        drawCube_glDrawElements1()
    
    glPopMatrix()
    glDisable(GL_LIGHTING)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
    for i in range(19):
        glBegin(GL_LINES)
        glColor3ub(120, 120, 120)
        glVertex3fv(np.array([-1.8, 0, -1.8+(i*.2)]))
        glVertex3fv(np.array([1.8, 0, -1.8+(i*.2)]))
        glVertex3fv(np.array([-1.8+(i*.2), 0., -1.8]))
        glVertex3fv(np.array([-1.8+(i*.2), 0., 1.8]))
        glEnd()

def cursor_callback(window, xpos, ypos):
    global pos, eye_x, eye_y, eye_z, at_x, at_y, at_z, up_x, up_y, up_z
    global isDrag, Elevation, Azimuth, u, v, w, x, y, z
    if isDrag == 1:
        if (pos[0] - xpos) < 0:
            d_pi = 0
        if (pos[1] - ypos) < 0:
            d_theta = 0
        dpi = (pos[0] - xpos)*0.00005
        dtheta = (pos[1] - ypos)*0.00003 
        if up_y == 1:
            Elevation -= dtheta
            Azimuth += dpi
        else:
            Elevation -= dtheta
            Azimuth -= dpi
        
    elif isDrag == 2:
        dx = (pos[0] - xpos)*0.00003
        dy = (pos[1] - ypos)*0.00003
        w = np.array([eye_x - at_x, eye_y - at_y, eye_z - at_z])
        w = w/np.sqrt(np.dot(w,w))
        v = np.array([up_x, up_y, up_z])
        u = np.cross(w,v)
        u = u/np.sqrt(np.dot(u, u))
        v = np.cross(w,u)
        v = v/np.sqrt(np.dot(v,v))
        u = u*dx
        v = v*-dy
        x = x + u[0]+v[0]
        y = y + u[1]+v[1]
        z = z + u[2]+v[2]

def set_cursor_none(window, xpos, ypos):
    return None

def mouse_button_callback(window, button, action, mod):
    global eye_x, eye_y, eye_z, left, right, bottom, top, zNear, zFar
    global pos, isDrag, u, v, w
    #ROTATION
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            isDrag = 1
            pos = glfw.get_cursor_pos(window)
            glfw.set_cursor_pos_callback(window, cursor_callback)          
        elif action == glfw.RELEASE:
            glfw.set_cursor_pos_callback(window, set_cursor_none)
            
    #PANNING
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            isDrag = 2
            pos = glfw.get_cursor_pos(window)
            glfw.set_cursor_pos_callback(window, cursor_callback)
        elif action == glfw.RELEASE:
            glfw.set_cursor_pos_callback(window, set_cursor_none)

def scroll_callback(window, xoffset, yoffset):
    global r
    if (r - 0.1*yoffset) < 0:
        pass
    else:
         r -= 0.1*yoffset
    
def drop_callback(window, paths):
    global gVertexArraySeparate, isDraw, vertex, index, arr, normal, isAvg, avg, avgnormal
    try:
        f = open(paths[0], 'r')
        fname = os.path.basename(paths[0])
        print('File name: ' + fname)
        vertex = []
        index = []
        normal = []
        avgnormal = []
        arr = []
        avg = []
        while True:
            line = f.readline()
            if not line:
                gVertexArraySeparate = createVertexArraySeparate()
                isAvg = 0
                isDraw = 1
                break
            parse(line) 
        f.close()
        glDisable(GL_LIGHTING)
    except IOError:
        print('object file not found')

cnt = 0
numvertex=0
avgnormal=[]
def parse(line):
    global vertex, normal, index, numvertex, arr, avg
    if 'v ' in line:
        v = line.split()
        vertex.append(((v[1]),(v[2]),(v[3])))
        numvertex+=1
        avgnormal.append((0,0,0))
        avgnormal.append(((v[1]),(v[2]),(v[3])))
    elif 'vn ' in line:
        avg = [[] for i in range(numvertex)]
        vn = line.split()
        normal.append((vn[1], vn[2], vn[3]))
    elif 'f ' in line:
        i = line.split()
        nor = np.array(normal, 'float32')
        index1 = i[1].split('/')
        index2 = i[2].split('/')
        index3 = i[3].split('/')
        index.append(((index1[0],index2[0],index3[0])))
        tmp = [0,0,0]
        #check
        tmp[0] += float(normal[int(index1[2])-1][0]) + float(normal[int(index2[2])-1][0]) + float(normal[int(index3[2])-1][0])
        tmp[1] += float(normal[int(index1[2])-1][1]) + float(normal[int(index2[2])-1][1]) + float(normal[int(index3[2])-1][1])
        tmp[2] += float(normal[int(index1[2])-1][2]) + float(normal[int(index2[2])-1][2]) + float(normal[int(index3[2])-1][2])

        arr.append(tmp)
        arr.append(vertex[int(index1[0])-1])
        arr.append(tmp)
        arr.append(vertex[int(index2[0])-1])
        arr.append(tmp)
        arr.append(vertex[int(index3[0])-1])

        #for S key 
        check1 = check2 = check3 = 0
        for i in range(0,len(avg[int(index1[0])-1])):
            if avg[int(index1[0])-1][i] == tmp:
                check1 = 1
        if check1 == 0:
            avg[int(index1[0])-1].append(tmp)

        for i in range(0,len(avg[int(index2[0])-1])):
            if avg[int(index2[0])-1][i] == tmp:
                check2 = 1
        if check2 == 0:
            avg[int(index2[0])-1].append(tmp)
            
        for i in range(0,len(avg[int(index3[0])-1])):
            if avg[int(index3[0])-1][i] == tmp:
                check3 = 1
        if check3 == 0:
            avg[int(index3[0])-1].append(tmp)
        
def createVertexArraySeparate():
    global vertex, index, normal, numvertex, arr, avgarr
    varr = np.array(arr, 'float32')
    iarr = np.array(index, 'int')
    
    tmp1 = tmp2 = 0
    num = np.zeros((1,3))
   
    for i in range(0, len(arr), 6):
        checkequal = 0
        for j in range(len(num)):
            if num[j][0] == arr[i][0] and num[j][1] == arr[i][1] and num[j][2] == arr[i][2]:
                checkequal=1
        if checkequal == 0:
            num = np.r_[num, [arr[i]]]

    tmp = np.zeros(len(num))
    
   
    for i in range(0, len(arr), 6):
       for j in range(1, len(num)):
           if arr[i][0] == num[j][0] and arr[i][1] == num[j][1] and arr[i][2] == num[j][2]:
               tmp[j]+=1

    for i in range(1,len(num)):
        if tmp[i] == 2:
            tmp1 +=1
        elif tmp[i] > 2:
            tmp2 +=1
    
    print('Total number of faces: ' + str(len(iarr) + tmp1 + tmp2))
    print('Number of faces with 3 vertices: ' + str(len(iarr)))
    print('Number of faces with 4 vertices: ' + str(tmp1))
    print('Number of faces with more than 4 vertices: ' + str(tmp2) + '\n')
    return varr

isDraw = 0

def drawCube_glDrawElements():
    global gVertexArraySeparate, isDraw
    if isDraw == 1:
        varr = gVertexArraySeparate
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
        glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

zcount = 0
scount = 0
isAvg = 0
def key_callback(window, key, scancode, action, mods):
    global zcount,scount, numvertex, avg, avgarr, isAvg, gVertexArrayIndexed, gIndexArray 
    if action==glfw.PRESS:
        if key==glfw.KEY_Z and zcount%2==0:
            glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
            zcount+=1
        elif key==glfw.KEY_Z and zcount%2==1:
            glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
            zcount+=1
        elif key==glfw.KEY_S and scount%2==0:
            isAvg = 1
            scount+=1
            avgarr = np.zeros((numvertex, 3), dtype='float32')
            #compute the average face normal vector         
            for i in range(0, numvertex):
                tmp = np.zeros(3)
                for j in range(0, len(avg[i])):
                    tmp[0] += float(avg[i][j][0])
                    tmp[1] += float(avg[i][j][1])
                    tmp[2] += float(avg[i][j][2])
                avgarr[i][0] = float(tmp[0])
                avgarr[i][1] = float(tmp[1])
                avgarr[i][2] = float(tmp[2])
                avgarr[i] = avgarr[i]/np.sqrt(avgarr[i]@avgarr[i])
            gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
        elif key==glfw.KEY_S and scount%2==1:
            scount+=1
            isAvg = 0

            
def drawCube_glDrawElements1():
    global gVertexArrayIndexed, gIndexArray, isDraw
    if isDraw == 1:
        varr = gVertexArrayIndexed
        iarr = gIndexArray
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
        glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
        glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
        
def createVertexAndIndexArrayIndexed():
    global avgnormal, index, avgarr, numvertex
    varr = np.array(avgnormal, 'float32')
    j = 0
    for i in range(0,len(avgnormal), 2):
        varr[i] = avgarr[j]
        j+=1
    iarr = np.array(index, 'int')
    iarr -= 1

    return varr, iarr
            
gVertexArraySeparate = None
gVertexArrayIndexed = None
gIndexArray = None

def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "2017030482_ClassAssignment2", None, None)
    if not window:
        glfw.ternminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)
        render()
        
    glfw.terminate()

if __name__ == "__main__":
    main()
