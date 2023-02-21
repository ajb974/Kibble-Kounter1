import KibbleKounter
import time

camera = KibbleKounter.setupCamera()
fname= KibbleKounter.takePicture(camera,'picture1')
print (fname) 
