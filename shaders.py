# SHADERS

import pymel.core as py
import maya.cmds as mc
import maya.mel as mel
from math import *
from xml.dom.minidom import *
from random import uniform as rnd
import os
import re
#~~
from mayatoolbox import *

def sCameraCubeCam(p = [0,0,0], r = [0,0,0], name="camera"):
    name = getUniqueName(name)
    target = camera(n=str(name))
    move(p[0],p[1],p[2])
    rotate(r[0],r[1],r[2])
    return target


def sCameraCube(ipd = 0.064):
    target = []

    target += sCameraCubeCam([-ipd,0,0], [0,0,0], "CameraNorthL") #northL
    target += sCameraCubeCam([ipd,0,0], [0,0,0], "CameraNorthR") #northR
    target += sCameraCubeCam([-ipd,0,0], [0,0,180], "CameraSouthL") #southL
    target += sCameraCubeCam([ipd,0,0], [0,0,180], "CameraSouthR") #southR
    target += sCameraCubeCam([-ipd,0,0], [0,90,0], "CameraUpL") #upL
    target += sCameraCubeCam([ipd,0,0], [0,90,0], "CameraUpR") #upR
    target += sCameraCubeCam([-ipd,0,0], [0,-90,0], "CameraDownL") #downL
    target += sCameraCubeCam([ipd,0,0], [0,-90,0], "CameraDownR") #downR
    #~~
    target += sCameraCubeCam([0,0,-ipd], [0,0,-90], "CameraEastL") #eastL
    target += sCameraCubeCam([0,0,ipd], [0,0,-90], "CameraEastR") #eastR
    target += sCameraCubeCam([0,0,-ipd], [0,0,90], "CameraWestL") #westL
    target += sCameraCubeCam([0,0,ipd], [0,0,90], "CameraWestR") #westR

    sl = spaceLocator(name="cameraRoot")

    for i in range(0,len(target)):
        try:
            parent(target[i],sl)
        except:
            print "Error parenting camera to locator."

    s(sl)

def revealYaxis():
    target = py.ls(sl=1)

    for i in range(0,len(target)):
        py.select(target[i])
        p = getPos()
        a = getAlpha()
        
        t(0)
        keyAlpha(0)
        
        delay = 10 * p[1]
        t(delay)
        keyAlpha(0)
        
        t(delay+10)
        keyAlpha(a)

def createShader(shaderType="lambert",shaderColor=[127,127,127,255],useTexture=False):
    #1. get selection
    target = py.ls(sl=1)
    #2. initialize shader
    shader=py.shadingNode(shaderType,asShader=True)
    #3. create a file texture node
    if(useTexture==True):
        file_node=py.shadingNode("file",asTexture=True)
    #4. create a shading group
    shading_group= py.sets(renderable=True,noSurfaceShader=True,empty=True)
    #5. set the color
    setRGBA(shader,shaderColor)
    #6. connect shader to sg surface shader
    py.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %shading_group)
    #7. connect file texture node to shader's color
    if(useTexture==True):
        py.connectAttr('%s.outColor' %file_node, '%s.color' %shader)
    #9. restore selection
    py.select(target)
    #10. return the completed shader
    return shader

def setShader(shader):
    py.hyperShade(a=shader)

def getShader():
    # get shapes of selection:
    shapesInSel = py.ls(dag=1,o=1,s=1,sl=1)
    # get shading groups from shapes:
    shadingGrps = py.listConnections(shapesInSel,type='shadingEngine')
    # get the shaders:
    shader = py.ls(py.listConnections(shadingGrps),materials=1)
    return shader[0] 

def quickShader(shaderColor=[255,0,0]):
    if(len(shaderColor)==3):
        shaderColor.append(255)
    shader = createShader("lambert",shaderColor,False)
    setShader(shader)
    return shader
    
#~~

#set RGBA, RGB, A at shader level
def setRGBA(s,c):
    r = float(c[0]) / 255.0
    g = float(c[1]) / 255.0
    b = float(c[2]) / 255.0
    a = abs(1-(float(c[3]) / 255.0))
    py.setAttr(s + ".color", (r,g,b))
    py.setAttr(s + ".transparency", (a,a,a))

def setRGB(s,c):
    r = float(c[0]) / 255.0
    g = float(c[1]) / 255.0
    b = float(c[2]) / 255.0
    py.setAttr(s + ".color", (r,g,b))

def setA(s,c):
    a = abs(1-(float(c) / 255.0))
    py.setAttr(s + ".transparency", (a,a,a))   

#~~

# set RGB color 0-255, any number of selections
def setColor(c):
    target = py.ls(sl=1)
    for i in range(0,len(target)):
        py.select(target[i])
        s = getShader()
        r = float(c[0]) / 255.0
        g = float(c[1]) / 255.0
        b = float(c[2]) / 255.0
        py.setAttr(s + ".color", (r,g,b))      

# returns RGB color 0-255 of first selection
def getColor():
    target = py.ls(sl=1)
    py.select(target[0])
    s = getShader()
    c = py.getAttr(s + ".color")   
    r = float(c[0]) / 255.0
    g = float(c[1]) / 255.0
    b = float(c[2]) / 255.0
    return (r,g,b)
#~~

# set transparency 0-255, any number of selections
def setAlpha(c):
    target = py.ls(sl=1)
    for i in range(0,len(target)):
        py.select(target[i])
        s = getShader()
        a = abs(1-(float(c) / 255.0))
        py.setAttr(s + ".transparency", (a,a,a))   

# returns transparency 0-255 from first selection
def getAlpha():
    target = py.ls(sl=1)
    py.select(target[0])
    s = getShader()
    aa = py.getAttr(s + ".transparency")
    a = 255 * abs(1-aa[0])
    return a

# keyframe transparency 0-255, any number of selections
def keyAlpha(c):
    target = py.ls(sl=1)
    for i in range(0,len(target)):
        py.select(target[i])
        s = getShader()
        setA(s,c)
        py.mel.eval("setKeyframe { \"" + s + ".it\" };")

