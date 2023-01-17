#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")

from math import pi, sin, cos

from panda3d.core import TextNode, GeomNode
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import GeomVertexArrayFormat, GeomVertexFormat
from panda3d.core import Geom, GeomNode, GeomLines
from panda3d.core import GeomVertexReader, GeomVertexWriter
from panda3d.core import GeomVertexRewriter, GeomVertexData

from direct.gui.OnscreenText import OnscreenText

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

import random, sys, os, math

class MyApp(ShowBase):
    #Macro-like function used to reduce the amount to code needed to create the
    #on screen instructions
    def genLabelText(self, text, i):
        return OnscreenText(text = text, pos = (-1.3, .95-.05*i), fg=(1,1,1,1),
                            align = TextNode.ALeft, scale = .05, mayChange = 1)

    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()

        # Pseudo-constants
        self.titleString = "Panda3D: Orbital Camera v0.016"
        self.renderRatio = 1.0e-6
        self.degPerSecond = 60.0
        self.minCameraDistance = 4.0
        self.maxCameraDistance = 4000.0
        self.zoomPerSecond = 1.8

        # Earth parameters
        self.earthSize = 6.37800000E+06
        self.earthRotationSpeed = 10.0 # Fake rotation in deg/sec for fast demo

        # Moon parameters
        self.moonSize = 1.73000000E+06
        self.moonRotationSpeed = 10.0 # Fake rotation in deg/sec for fast demo
        self.moonOrbitalDistance = 3.88960000E+08
        self.moonOrbitalSpeed = 20.0 # Fake orbital speed in deg/sec for fast demo
        self.moonRenderOrbitalDistance = self.moonOrbitalDistance * self.renderRatio
        self.moonOrbitNumberPoints = 360

        #Make the background color black (R=0, G=0, B=0)
        #instead of the default grey
        base.setBackgroundColor(0, 0, 0)

        # Init camera move variables
        self.keyMap = {"left":0, "right":0, "up":0, "down":0, "pageup":0, "pagedown":0, "wheelup":0, "wheeldown":0, "mouse3":0, "tab":0}
        self.angleLongitudeDegrees = 0.0
        self.angleLatitudeDegrees = 0.0
        self.cameraDistance = 10.0
        self.targetNode = render

        #This code puts the standard title and instruction text on screen
        self.titleText = OnscreenText(text=self.titleString,
                                      style=1, fg=(1,1,0,1),
                                      pos=(0.8,-0.95), scale = .07)

        # Create empty node for world origin
        self.worldOrigin = render.attachNewNode("World Origin")

        # Load the Earth model
        self.earth = loader.loadModel("models/planet_sphere")
        self.earth_tex = loader.loadTexture("models/earth_1k_tex.jpg")
        self.earth.setTexture(self.earth_tex, 1)
        self.earth.reparentTo(self.worldOrigin)
        self.earth.setScale(self.earthSize * self.renderRatio)
        self.earth.setPos(0.0, 0.0, 0.0)
        self.earth.setTag('targetSize', str(self.earthSize))

        # Load the Moon model
        self.moon = loader.loadModel("models/planet_sphere")
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.moon.setTexture(self.moon_tex, 1)
        self.moon.reparentTo(self.worldOrigin)
        self.moon.setScale(self.moonSize * self.renderRatio)
        self.moon.setPos(self.moonOrbitalDistance * self.renderRatio, 0.0, 0.0)
        self.moon.setTag('targetSize', str(self.moonSize))

        # Create and populate the Moon orbit model using Vertices and Lines
        self.moonOrbitVertexData = GeomVertexData('moonOrbitVertexData', GeomVertexFormat.getV3(), Geom.UHDynamic)
        self.moonOrbitVertexWriter = GeomVertexWriter(self.moonOrbitVertexData, 'vertex')

        for i in range(self.moonOrbitNumberPoints):
            angleDegrees = i * 360 / self.moonOrbitNumberPoints
            angleRadians = angleDegrees * (pi / 180.0)
            x = -self.moonRenderOrbitalDistance * sin(angleRadians)
            y =  self.moonRenderOrbitalDistance * cos(angleRadians)
            self.moonOrbitVertexWriter.addData3f(x, y, 0.0)
        self.moonOrbitLines = GeomLines(Geom.UHStatic)
       	
        for i in range(self.moonOrbitNumberPoints-1):
            self.moonOrbitLines.addVertex(i)
            self.moonOrbitLines.addVertex(i+1)
            self.moonOrbitLines.closePrimitive()
        self.moonOrbitLines.addVertex(self.moonOrbitNumberPoints-1)
        self.moonOrbitLines.addVertex(0)
        self.moonOrbitLines.closePrimitive()
        self.moonOrbitGeom = Geom(self.moonOrbitVertexData)
        self.moonOrbitGeom.addPrimitive(self.moonOrbitLines)
        self.moonOrbitNode = GeomNode('moonOrbitNode')
        self.moonOrbitNode.addGeom(self.moonOrbitGeom)
        self.moonOrbitNnodePath = render.attachNewNode(self.moonOrbitNode)
        self.moonOrbitNnodePath.reparentTo(self.worldOrigin)

        # Setup events for escape : exit from app
        self.accept("escape", sys.exit)

        # Setup down events for arrow keys : rotating camera latitude and longitude
        self.accept("arrow_left", self.setKey, ["left",1])
        self.accept("arrow_right", self.setKey, ["right",1])
        self.accept("arrow_up", self.setKey, ["up",1])
        self.accept("arrow_down", self.setKey, ["down",1])
        self.accept("page_up", self.setKey, ["pageup",1])
        self.accept("page_down", self.setKey, ["pagedown",1])

        # Setup up events for control keys
        self.accept("arrow_left-up", self.setKey, ["left",0])
        self.accept("arrow_right-up", self.setKey, ["right",0])
        self.accept("arrow_up-up", self.setKey, ["up",0])
        self.accept("arrow_down-up", self.setKey, ["down",0])
        self.accept("page_up-up", self.setKey, ["pageup",0])
        self.accept("page_down-up", self.setKey, ["pagedown",0])

        # Setup events for mouse wheel
        self.accept("wheel_up", self.setKey, ["wheelup",1])
        self.accept("wheel_down", self.setKey, ["wheeldown",1])

        # Setup events for the Left Mouse Button : picking
        self.accept("mouse1", self.pickFromCamera)

        # Setup events for the Right Mouse Button : rotating camera latitude and longitude
        self.accept("mouse3", self.setKey, ["mouse3",1])
        self.accept("mouse3-up", self.setKey, ["mouse3",0])

        # Setup a Tab event for switching target
        self.accept("tab", self.setKey, ["tab",1])
        self.accept("tab-up", self.setKey, ["tab",0])

        # Attach the camera to the Earth to begin with
        self.targetNode = self.earth
        self.targetSize = float(self.targetNode.getTag("targetSize"))

        # Create picker Node and CollisionRay
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)

        # Create Collision Traverser and Queue
        self.cameraPickingTraverser = CollisionTraverser('Camera Picking Traverser')
        self.cameraPickingQueue = CollisionHandlerQueue()

        # Link Picker Node to Traverser and Queue
        self.cameraPickingTraverser.addCollider(self.pickerNP, self.cameraPickingQueue)

        # Set tags on Earth and Moon to be pickable
        self.earth.setTag('isPickable', '1')
        self.moon.setTag('isPickable', '2')

        # Add text to display the camera position
        self.displayCameraDistanceText = self.genLabelText("Camera distance : " + str(self.cameraDistance * self.earthSize) + " m", 0)
        self.displayCameraLatitudeText = self.genLabelText("Camera latitude : " + str(self.angleLatitudeDegrees) + " deg", 1)
        self.displayCameraLongitudeText = self.genLabelText("Camera longitude : " + str(self.angleLongitudeDegrees) + " deg", 2)
        self.displayTargetNodePositionText = self.genLabelText("Target position : (" + str(self.targetNode.getX()) + "; " + str(self.targetNode.getY()) + "; " + str(self.targetNode.getZ()) + ")", 3)

        # Add tasks to move the planets
        self.taskMgr.add(self.rotateEarth, "rotateEarth", sort=1)
        self.taskMgr.add(self.rotateMoon, "rotateMoon", sort=1)
        self.taskMgr.add(self.moveMoonOrbit, "moveMoonOrbit", sort=1)

        # Add task to manage the camera
        # Task sort parameters are set so camera task is last to execute
        self.taskMgr.add(self.moveOrbitalCameraTask, "moveOrbitalCameraTask", sort=2)

    # Define a function to deal with camera picking collisions
    # Must be called from the "mouse1" event
    def pickFromCamera(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

        self.cameraPickingTraverser.traverse(render)

        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
        if self.cameraPickingQueue.getNumEntries() > 0:
            # This is so we get the closest object.
            self.cameraPickingQueue.sortEntries()
            pickedObj = self.cameraPickingQueue.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetTag('isPickable')
            if not pickedObj.isEmpty():
                self.targetNode = pickedObj
                self.targetSize = float(self.targetNode.getTag("targetSize"))

    # Define a procedure to move the camera.
    # In fact, never moves the camera, but instead the world origin
    # But always keeps the camera oriented towards the world origin
    def moveOrbitalCameraTask(self, task):
        # Get mouse
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()

        if (self.keyMap["tab"]!=0):
            if (self.targetNode == self.earth):
                self.targetNode = self.moon
            else:
                self.targetNode = self.earth
            self.setKey("tab",0)
            self.targetSize = float(self.targetNode.getTag("targetSize"))

        if (self.keyMap["mouse3"]!=0):
            # Use mouse moves to change longitude and latitude
            self.angleLongitudeDegrees = self.angleLongitudeDegrees - (x - self.lastMouseX) * 0.2
            self.angleLatitudeDegrees = self.angleLatitudeDegrees - (y - self.lastMouseY) * 0.2
            # Restore position as frozen when the MB1 was depressed
            #base.win.movePointer(0, self.mouseFreezeX, self.mouseFreezeX)

        # Store latest mouse position for the next frame
        self.lastMouseX = x
        self.lastMouseY = y

        # First compute new camera angles and distance
        if (self.keyMap["left"]!=0):
            self.angleLongitudeDegrees = self.angleLongitudeDegrees - self.degPerSecond * globalClock.getDt()
        if (self.keyMap["right"]!=0):
            self.angleLongitudeDegrees = self.angleLongitudeDegrees + self.degPerSecond * globalClock.getDt()
        if (self.keyMap["up"]!=0):
            self.angleLatitudeDegrees = self.angleLatitudeDegrees - self.degPerSecond * globalClock.getDt()
        if (self.keyMap["down"]!=0):
            self.angleLatitudeDegrees = self.angleLatitudeDegrees + self.degPerSecond * globalClock.getDt()
        if (self.keyMap["pageup"]!=0 or self.keyMap["wheelup"]!=0):
            self.cameraDistance = self.cameraDistance * (1 + (self.zoomPerSecond-1) * globalClock.getDt())
            self.setKey("wheelup",0)
        if (self.keyMap["pagedown"]!=0 or self.keyMap["wheeldown"]!=0):
            self.cameraDistance = self.cameraDistance / (1 + (self.zoomPerSecond-1) * globalClock.getDt())
            self.setKey("wheeldown",0)

        # Limit angles to [-180;+180]x[-90;+90] and distance between set min and max
        if (self.angleLongitudeDegrees > 180.0):
            self.angleLongitudeDegrees = self.angleLongitudeDegrees - 360.0
        if (self.angleLongitudeDegrees < -180.0):
            self.angleLongitudeDegrees = self.angleLongitudeDegrees + 360.0
        if (self.angleLatitudeDegrees > (90.0 - 0.001)):
            self.angleLatitudeDegrees = 90.0 - 0.001
        if (self.angleLatitudeDegrees < (-90.0 + 0.001)):
            self.angleLatitudeDegrees = -90.0 + 0.001
        if (self.cameraDistance < self.minCameraDistance):
            self.cameraDistance = self.minCameraDistance
        if (self.cameraDistance > self.maxCameraDistance):
            self.cameraDistance = self.maxCameraDistance

        # Convert to Radians
        angleLongitudeRadians = self.angleLongitudeDegrees * (pi / 180.0)
        angleLatitudeRadians = self.angleLatitudeDegrees * (pi / 180.0)

        # Compute the target object's position with respect to the camera
        x = -self.cameraDistance * self.targetSize * sin(angleLongitudeRadians) * cos(angleLatitudeRadians)
        y =  self.cameraDistance * self.targetSize * cos(angleLongitudeRadians) * cos(angleLatitudeRadians)
        z =  self.cameraDistance * self.targetSize * sin(angleLatitudeRadians)

        # Compute the world origin's position with respect to the camera
        x = (x * self.renderRatio) - self.targetNode.getX(self.worldOrigin)
        y = (y * self.renderRatio) - self.targetNode.getY(self.worldOrigin)
        z = (z * self.renderRatio) - self.targetNode.getZ(self.worldOrigin)

        # Apply the position
        self.worldOrigin.setPos(x, y, z)

        # Rotate the camera
        self.camera.setHpr(self.angleLongitudeDegrees, self.angleLatitudeDegrees, 0)

        # Display camera position
        self.displayCameraDistanceText.setText("Camera distance : " + str(self.cameraDistance * self.targetSize) + " m")
        self.displayCameraLatitudeText.setText("Camera latitude : " + str(self.angleLatitudeDegrees) + " deg")
        self.displayCameraLongitudeText.setText("Camera longitude : " + str(self.angleLongitudeDegrees) + " deg")
        self.displayTargetNodePositionText.setText("Target position : (" + str(self.targetNode.getX()) + "; " + str(self.targetNode.getY()) + "; " + str(self.targetNode.getZ()) + ")")

        # End task
        return Task.cont

    def rotateEarth(self, task):
        # Compute earth rotation
        frameTime = globalClock.getFrameTime()
        angleDegrees = frameTime *  self.earthRotationSpeed
        self.earth.setHpr(angleDegrees, 0, 0)

        # End task
        return Task.cont

    def rotateMoon(self, task):
        # Compute earth rotation
        frameTime = globalClock.getFrameTime()
        angleDegrees = frameTime *  self.moonRotationSpeed
        self.moon.setHpr(angleDegrees, 0, 0)

        # End task
        return Task.cont

    def moveMoonOrbit(self, task):
        # Compute Moon position relative to Earth with circular orbit
        frameTime = globalClock.getFrameTime()
        angleDegrees = frameTime *  self.moonOrbitalSpeed
        angleRadians = angleDegrees * (pi / 180.0)

        # Compute the Moon's position with respect to the Earth
        x = -self.moonRenderOrbitalDistance * sin(angleRadians)
        y =  self.moonRenderOrbitalDistance * cos(angleRadians)

        # Set the position on the model
        self.moon.setPos(x, y, 0.0)

        # Also rotate the orbit to follow the Moon and eliminate jitter effect
        self.moonOrbitVertexWriter.setRow(0)
        for i in range(self.moonOrbitNumberPoints):
            angleDegrees = angleDegrees + 360.0 / self.moonOrbitNumberPoints
            angleRadians = angleDegrees * (pi / 180.0)
            x = -self.moonRenderOrbitalDistance * sin(angleRadians)
            y =  self.moonRenderOrbitalDistance * cos(angleRadians)
            self.moonOrbitVertexWriter.setData3f(x, y, 0.0)

        # End task
        return Task.cont

    #Records the state of the keyboard and mouse
    def setKey(self, key, value):
        # Store mouse position at the time of freeze
        if (key == "mouse3"):
            md = base.win.getPointer(0)
            self.lastMouseX = md.getX()
            self.lastMouseY = md.getY()
        #Store key/button press/release
        self.keyMap[key] = value
        # Display latest key change
        #if (value == 0):
        #    self.titleText.setText(key + " up")
        #else:
        #    self.titleText.setText(key + " down")

app = MyApp()
app.run()

"""
from spaceman3D.Draw import Draw
from spaceman3D.Orbit import satellites

#Create a class instance of Draw()
d = Draw()

#Call the draw Orbit function
#d.draw_orbit(satellites.ISS, satellites.Dragon, object='Earth')

#or What would the Satellite look like around the Moon
d.draw_orbit(satellites.Dragon, object='Moon')
"""