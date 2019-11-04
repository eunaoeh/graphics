import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

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
offset = []
isDraw = 0
tmp = 0
endcnt = 0
fname = ''

def render():
    global eye_x,eye_y,eye_z, at_x, at_y, at_z, up_x, up_y, up_z, Elevation, Azimuth, r, x, y, z
    global isDraw, offset, tmp, endcnt, fname
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.01, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if np.cos(Elevation) < 0:
        up_y = -1
    else:
        up_y = 1
    eye_y = r*np.sin(Elevation) + at_x
    eye_z = r*np.cos(Elevation)*np.cos(Azimuth) + at_y
    eye_x = r*np.cos(Elevation)*np.sin(Azimuth) + at_z
    gluLookAt(eye_x-x, eye_y-y, eye_z-z, at_x-x, at_y-y, at_z-z, up_x, up_y, up_z)
    r = np.sqrt(np.square(eye_x-at_x)+np.square(eye_y-at_y)+np.square(eye_z-at_z))

    drawFrame()
    glColor3ub(255,255,255)
    if fname == 'sample-walk.bvh':
        glEnable(GL_LIGHTING)   # try to uncomment: no lighting
        glEnable(GL_LIGHT0)

        glEnable(GL_RESCALE_NORMAL)
        
        # light position
        glPushMatrix()

        glLightfv(GL_LIGHT0, GL_POSITION, (3.,3.,3.,0.))
        glPopMatrix()

        # light intensity for each color channel
        lightColor = (1.,1.,1.,1.)
        ambientLightColor = (.1,.1,.1,1.)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

        # material reflectance for each color channel
        objectColor = (0.3,0.3,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

        glPushMatrix()
    
    if isDraw == 1:
        drawHierarchy()
    elif isDraw == 2:
        drawMotionHierarchy(tmp)
        tmp += 1
        if tmp >= len(frame)/(len(name_joint) + 1):
            tmp = 0
            offset[0][0] = 0
            offset[0][1] = 0
            offset[0][2] = 0
            endcnt = 0
        
    if fname == 'sample-walk.bvh':
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
    global offset, frame, channel, num_channel, motion, name_joint, num_frame, fps, cnt, isDraw, check_end, tmp
    global fname, tmp, gVertexArraySeparate
    try:
        f = open(paths[0], 'r')
        fname = os.path.basename(paths[0])
        offset = []
        name_joint = []
        num_frame = 0
        fps = 0
        check_end = 0
        cnt = 0
        isDraw = 0
        check_end = 0
        motion = 0
        frame = []
        channel = []
        tmp = 0
        num_channel = 0
        print('File name: ' + fname)
        while True:
            line = f.readline()
            if not line:
                print_info()
                break
            parse(line)
        isDraw = 1
        f.close()
    except IOError:
        print('object file not found')

check_end = 0
def parse(line):
    global offset, num_channel, name_joint, num_frame, fps, cnt, check_end, motion, frame
    if 'ROOT' in line:
        line = line.split()
        name_joint.append((line[1]))
    elif 'OFFSET' in line:
        line = line.split()
        offset.append(([float(line[1]),float(line[2]),float(line[3])]))
    elif 'CHANNELS' in line:
        line = line.split()
        num_channel += int(line[1]) # total number of Channels
        if int(line[1]) == 3:
            for i in range(3):
                channel.append([line[2],line[3],line[4]]) # Channel
        elif int(line[1]) == 6:
            for i in range(3):
                channel.append([line[5],line[6],line[7]]) # Channel
    elif 'JOINT' in line:
        if check_end == 1:
            offset.append([cnt])
            cnt = 0 # count the number of }'s
            check_end = 0
        line = line.split()
        name_joint.append(line[1]) # Name of Joint
    elif 'End Site' in line:
        check_end = 1
    elif '{' in line:
        pass
    elif '}' in line:
        cnt += 1 # For how many pop
    elif 'MOTION' in line:
        motion = 1
    elif 'Frames:' in line:
        line = line.split()
        num_frame = line[1] # number of frames
    elif 'Frame Time:' in line:
        line = line.split()
        fps = line[2] # FPS
    else:
        if motion == 1: # Motion Frame in list
            line = line.split()
            for i in range(0, len(line),3):
                frame.append([float(line[i]), float(line[i+1]), float(line[i+2])])

def print_info():
    print('Number of frames: ' + num_frame)
    print('FPS: ' + str(1/float(fps)))
    print('Number of joints: ' + str(len(name_joint)))
    print('List of all joint names: ' + str(name_joint) + '\n')

def drawHierarchy():    
    global offset, fname, gVertexArraySeparate
    glColor3ub(80,80,255)
    check = 0
    popcnt = 0
    pushcnt = 0
    for i in range(1, len(offset)):
        if len(offset[i]) == 1:
            for j in range(offset[i][0] - 1):
                glPopMatrix()
                i += 1
                check = 1
                popcnt += 1
        else:
            if check == 0:
                pushcnt += 1
                glPushMatrix()
                glTranslatef(offset[i-1][0], offset[i-1][1], offset[i-1][2])
                glPushMatrix()
                if fname == 'sample-walk.bvh':
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/4, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0:
                            a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0, offset[i][1]/4, 0)
                        b = abs(offset[i][1])/2
                        if b == 0:
                            b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/4)
                        c = abs(offset[i][2])/2
                        if c == 0:
                            c = .03
                        a = b = .03
                    gVertexArraySeparate=createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    drawLine([0,0,0], offset[i])
                    glPopMatrix()        
            else:
                check = 0
                if fname == 'sample-walk.bvh':
                    glPushMatrix()
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/4, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0:
                            a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0,  offset[i][1]/4, 0)
                        b = abs(offset[i][1])/2
                        if b == 0:
                            b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/4)
                        c = abs(offset[i][2])/2
                        if c == 0:
                            c = .03
                        a = b = .03

                    gVertexArraySeparate = createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    drawLine([0,0,0], offset[i])
    for i in range(pushcnt - popcnt):
        glPopMatrix()


def drawLine(a, b):
    glBegin(GL_LINES)
    glVertex3fv(np.array(a))
    glVertex3fv(np.array(b))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global offset, frame, num_channel, channel, num_frame, isDraw    
    if key == glfw.KEY_SPACE:
        if action == glfw.PRESS:
            isDraw = 2

def drawMotionHierarchy(k):
    global channel, offset, fname,gVertexArraySeparate
    glColor3ub(80,80,255)
    check = 0
    popcnt = 0
    pushcnt = 0
    endcnt = 0
    
    glPushMatrix()
    glTranslatef(frame[k*(len(name_joint)+1)][0],frame[k*(len(name_joint)+1)][1],frame[k*(len(name_joint)+1)][2])
   
    for i in range(1, len(offset)):
        if len(offset[i]) == 1:
            endcnt+=1
            for j in range(offset[i][0] - 1):
                glPopMatrix()
                i += 1
                check = 1
                popcnt += 1
        else:
            if check == 0:
                pushcnt += 1
                glPushMatrix()
                
                glTranslatef(offset[i-1][0], offset[i-1][1], offset[i-1][2])    
                Rotation(i,i-endcnt+k*int(len(name_joint)+1))
                
                glPushMatrix()
                if fname == 'sample-walk.bvh':
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/3, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0:
                            a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0,  offset[i][1]/3, 0)
                        b = abs(offset[i][1])/2
                        if b == 0:
                            b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/3)
                        c = abs(offset[i][2])/2
                        if c == 0:
                            c = .03
                        a = b = .03
                    gVertexArraySeparate=createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    drawLine([0,0,0], offset[i])
                    glPopMatrix()
            else:
                check = 0
                endcnt += 1

                if fname == 'sample-walk.bvh':
                    glPushMatrix()
                    if abs(offset[i][0]) >= abs(offset[i][1]) and abs(offset[i][0]) >= abs(offset[i][2]):
                        glTranslatef(offset[i][0]/3, 0, 0)
                        a = abs(offset[i][0])/2
                        if a == 0:
                            a = .03
                        b = c = .03
                    elif abs(offset[i][1]) >= abs(offset[i][0]) and abs(offset[i][1]) >= abs(offset[i][2]):
                        glTranslatef(0,  offset[i][1]/3, 0)
                        b = abs(offset[i][1])/2
                        if b == 0:
                            b = .03
                        a = c = .03
                    elif abs(offset[i][2]) >= abs(offset[i][1]) and abs(offset[i][2]) >= abs(offset[i][0]):
                        glTranslatef(0, 0, offset[i][2]/3)
                        c = abs(offset[i][2])/2
                        if c == 0:
                            c = .03
                        a = b = .03
                    gVertexArraySeparate=createVertexArraySeparate(a, b, c)
                    drawCube_glDrawArray()
                    glPopMatrix()
                else:
                    drawLine([0,0,0], offset[i])
                    
    for i in range(pushcnt - popcnt):
        glPopMatrix()
    glPopMatrix()

def Rotation(i, num):
    global channel, frame
    if 'Z' in channel[i][0] and 'X' in channel[i][1] and 'Y' in channel[i][2]:
        glRotatef(frame[num][0], 0, 0, 1)
        glRotatef(frame[num][1], 1, 0, 0)
        glRotatef(frame[num][2], 0, 1, 0)
    elif 'Z' in channel[i][0] and 'Y' in channel[i][1] and 'X' in channel[i][2]:    
        glRotatef(frame[num][0], 0, 0, 1)
        glRotatef(frame[num][1], 0, 1, 0)
        glRotatef(frame[num][2], 1, 0, 0)
    elif 'Y' in channel[i][0] and 'X' in channel[i][1] and 'Z' in channel[i][2]:    
        glRotatef(frame[num][0], 0, 1, 0)
        glRotatef(frame[num][1], 1, 0, 0)
        glRotatef(frame[num][2], 0, 0, 1)
    elif 'Y' in channel[i][0] and 'Z' in channel[i][1] and 'X' in channel[i][2]:    
        glRotatef(frame[num][0], 0, 1, 0)
        glRotatef(frame[num][1], 0, 0, 1)
        glRotatef(frame[num][2], 1, 0, 0)
    elif 'X' in channel[i][0] and 'Y' in channel[i][1] and 'Z' in channel[i][2]:    
        glRotatef(frame[num][0], 1, 0, 0)
        glRotatef(frame[num][1], 0, 1, 0)
        glRotatef(frame[num][2], 0, 0, 1)
    elif 'X' in channel[i][0] and 'Z' in channel[i][1] and 'Y' in channel[i][2]:    
        glRotatef(frame[num][0], 1, 0, 0)
        glRotatef(frame[num][1], 0, 0, 1)
        glRotatef(frame[num][2], 0, 1, 0)

def createVertexArraySeparate(a, b, c):
    varr = np.array([
            (0,0,1),         # v0 normal
            ( -a ,  b ,  c ), # v0 position
            (0,0,1),         # v2 normal
            (  a , -b ,  c ), # v2 position
            (0,0,1),         # v1 normal
            (  a ,  b ,  c ), # v1 position

            (0,0,1),         # v0 normal
            ( -a ,  b ,  c ), # v0 position
            (0,0,1),         # v3 normal
            ( -a , -b ,  c ), # v3 position
            (0,0,1),         # v2 normal
            (  a , -b ,  c ), # v2 position

            (0,0,-1),
            ( -a ,  b , -c ), # v4
            (0,0,-1),
            (  a ,  b , -c ), # v5
            (0,0,-1),
            (  a , -b , -c ), # v6

            (0,0,-1),
            ( -a ,  b , -c ), # v4
            (0,0,-1),
            (  a , -b , -c ), # v6
            (0,0,-1),
            ( -a , -b , -c ), # v7

            (0,1,0),
            ( -a ,  b ,  c ), # v0
            (0,1,0),
            (  a ,  b ,  c ), # v1
            (0,1,0),
            (  a ,  b , -c ), # v5
            
            (0,1,0),
            ( -a ,  b ,  c ), # v0
            (0,1,0),
            (  a ,  b , -c ), # v5
            (0,1,0),
            ( -a ,  b , -c ), # v4

            (0,-1,0),
            ( -a , -b ,  c ), # v3
            (0,-1,0),
            (  a , -b , -c ), # v6
            (0,-1,0),
            (  a , -b ,  c ), # v2

            (0,-1,0),
            ( -a , -b ,  c ), # v3
            (0,-1,0),
            ( -a , -b , -c ), # v7
            (0,-1,0),
            (  a , -b , -c ), # v6

            (1,0,0),
            (  a ,  b ,  c ), # v1
            (1,0,0),
            (  a , -b ,  c ), # v2
            (1,0,0),
            (  a , -b , -c ), # v6

            (1,0,0),
            (  a ,  b ,  c ), # v1
            (1,0,0),
            (  a , -b , -c ), # v6
            (1,0,0),
            (  a ,  b , -c ), # v5

            (-1,0,0),
            ( -a ,  b ,  c ), # v0
            (-1,0,0),
            ( -a , -b , -c ), # v7
            (-1,0,0),
            ( -a , -b ,  c ), # v3

            (-1,0,0),
            ( -a ,  b ,  c ), # v0
            (-1,0,0),
            ( -a ,  b , -c ), # v4
            (-1,0,0),
            ( -a , -b , -c ), # v7
            ], 'float32')
    return varr

def drawCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

gVertexArraySeparate = None
def main():
    global gVertexArraySeparate
    global a,b,c
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "2017030482_ClassAssignment3", None, None)
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
