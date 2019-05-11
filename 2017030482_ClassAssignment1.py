import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

Azimuth = np.radians(60)
Elevation = np.radians(45)
r = 2
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

def render():
    global eye_x,eye_y,eye_z, at_x, at_y, at_z, up_x, up_y, up_z
    global Elevation, Azimuth, r, x, y, z
    
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
    drawPerson()

        
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

def drawPerson():
    t = glfw.get_time()

    #head
    glPushMatrix()
    glTranslatef(0, .7, 0)
    
    glPushMatrix()
    glScalef(.13, .13, .13)
    glColor3ub(255, 255, 255)
    drawSphere()
    glPopMatrix()

    #body
    glPushMatrix()
    glTranslatef(0, -.4, 0)

    glPushMatrix()
    glScalef(.17, .3, .17)
    glColor3ub(255, 255, 255)
    drawCube()
    glPopMatrix()

    #right arm
    glPushMatrix()
    glTranslatef(-.225, .25, 0)
    glRotatef(60*np.cos(t), 1, 0, 0)

    glPushMatrix()
    glScalef(.05, .15, .05)
    glColor3ub(255, 255, 255)
    drawCubeNotOrigin()
    glPopMatrix()

    #right arm2
    glPushMatrix()
    glTranslatef(0, -.3, 0)
    glRotatef(-90, 1, 0, 0)

    glPushMatrix()
    glScalef(.04, .12, .04)
    glColor3ub(255, 100, 100)
    drawCubeNotOrigin()
    glPopMatrix()

    #right hand
    glPushMatrix()
    glTranslatef(0, -0.3, 0)

    glPushMatrix()
    glScalef(0.06, 0.06, 0.06)
    glColor3ub(255, 255, 255)
    drawSphere()
    glPopMatrix()

    #right arms pop
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    #left arm
    glPushMatrix()
    glTranslatef(.225, .25, 0)
    glRotatef(60*np.cos(t + np.pi), 1, 0, 0)

    glPushMatrix()
    glScalef(.05, .15, .05)
    glColor3ub(255, 255, 255)
    drawCubeNotOrigin()
    glPopMatrix()

    #left arm2
    glPushMatrix()
    glTranslatef(0, -.3, 0)
    glRotatef(-90, 1, 0, 0)

    glPushMatrix()
    glScalef(.04, .12, .04)
    glColor3ub(255, 100, 100)
    drawCubeNotOrigin()
    glPopMatrix()

    #left hand
    glPushMatrix()
    glTranslatef(0, -0.3, 0)

    glPushMatrix()
    glScalef(0.06, 0.06, 0.06)
    glColor3ub(255, 255, 255)
    drawSphere()
    glPopMatrix()

    #left arms pop
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    #right leg
    glPushMatrix()
    glTranslatef(-.09, -.3, 0)
    glRotatef(60*np.cos(t + np.pi), 1, 0, 0)

    glPushMatrix()
    glScalef(.05, .15, .05)
    glColor3ub(100, 100, 255)
    
    drawCubeNotOrigin()
    glPopMatrix()

    #right knee
    glPushMatrix()
    glTranslatef(0, -0.3, 0)

    glPushMatrix()
    glScalef(0.06, 0.06, 0.06)
    glColor3ub(125, 125, 255)
    drawSphere()
    glPopMatrix()

    #right leg2
    glPushMatrix()
    glRotatef(70, 1, 0, 0)

    glPushMatrix()
    glScalef(.05, .15, .05)
    glColor3ub(150, 150, 255)
    drawCubeNotOrigin()
    glPopMatrix()

    #right foot
    glPushMatrix()
    glTranslatef(0, -.3, 0.05)

    glPushMatrix()
    glScalef(.05, .05, .12)
    glColor3ub(150, 255, 150)
    drawSphere()
    glPopMatrix()

    #right leg pop
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    #left leg
    glPushMatrix()
    glTranslatef(.09, -.3, 0)
    glRotatef(60*np.cos(t), 1, 0, 0)

    glPushMatrix()
    glScalef(.05, .15, .05)
    glColor3ub(100, 100, 255)
    drawCubeNotOrigin()
    glPopMatrix()

    #left knee
    glPushMatrix()
    glTranslatef(0, -0.3, 0)

    glPushMatrix()
    glScalef(0.06, 0.06, 0.06)
    glColor3ub(125, 125, 255)
    drawSphere()
    glPopMatrix()

    #left leg2
    glPushMatrix()
    glRotatef(70, 1, 0, 0)

    glPushMatrix()
    glScalef(.05, .15, .05)
    glColor3ub(150, 150, 255)
    drawCubeNotOrigin()
    glPopMatrix()

    #left foot
    glPushMatrix()
    glTranslatef(0, -.3, 0.05)

    glPushMatrix()
    glScalef(.05, .05, .12)
    glColor3ub(150, 255, 150)
    drawSphere()
    glPopMatrix()

    #left leg pop
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    glPopMatrix() #body
    glPopMatrix() #head
    
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

def drawCube():
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
    
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def drawCubeNotOrigin():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 0,-1.0)
    glVertex3f(-1.0, 0,-1.0)
    glVertex3f(-1.0, 0, 1.0)
    glVertex3f( 1.0, 0, 1.0)
    
    glVertex3f( 1.0,-2.0, 1.0)
    glVertex3f(-1.0,-2.0, 1.0)
    glVertex3f(-1.0,-2.0,-1.0)
    glVertex3f( 1.0,-2.0,-1.0)
    
    glVertex3f( 1.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.0, 1.0)
    glVertex3f(-1.0,-2.0, 1.0)
    glVertex3f( 1.0,-2.0, 1.0)
    
    glVertex3f( 1.0,-2.0,-1.0)
    glVertex3f(-1.0,-2.0,-1.0)
    glVertex3f(-1.0, 0.0,-1.0)
    glVertex3f( 1.0, 0.0,-1.0)
    
    glVertex3f(-1.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.0,-1.0)
    glVertex3f(-1.0,-2.0,-1.0)
    glVertex3f(-1.0,-2.0, 1.0)
    
    glVertex3f( 1.0, 0.0,-1.0)
    glVertex3f( 1.0, 0.0, 1.0)
    glVertex3f( 1.0,-2.0, 1.0)
    glVertex3f( 1.0,-2.0,-1.0)
    glEnd()

def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)

        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()
    
def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "2017030482 project 1", None, None)

    if not window:
        glfw.ternminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)
        render()
        
    glfw.terminate()

if __name__ == "__main__":
    main()
