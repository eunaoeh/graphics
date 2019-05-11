import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0

def render(gCamAng):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1,1, -1,1, -1,1)
 # rotate "camera" position to see this 3D space better (we'll see details later)
    gluLookAt(.1*np.sin(gCamAng),.05, .1*np.cos(gCamAng), 0,0,0, 0,1,0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    #drawFrame()
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

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
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

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gComposedM
    newM = np.identity(4)
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)

def main():
    global gCamAng
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "assignment-2", None, None)

    if not window:
        glfw.ternminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)
        render(gCamAng)
        
    glfw.terminate()

if __name__ == "__main__":
    main()
