import KibbleKounter
import time
import traceback
try:
    camera = KibbleKounter.setupCamera()
    fname= KibbleKounter.takePicture(camera,'picture1')
    print (fname) 
except Exception:
    traceback.print_exc()

try: 
    input("Zero Scale") 
    KibbleKounter.zeroScale() 
    input("Test Weight") 
    KibbleKounter.TestScale() 
    while True:
        print(str(KibbleKounter.readScale_grams()))
        time.sleep(0.5)
except Exception:
    traceback.print_exc()
