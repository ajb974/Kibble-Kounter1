import KibbleKounter
import time
import traceback
import spidev

def Adc_read(spi): #reads from channel 0, given spi object
    read=spi.xfer2([0x01,0b10000000,0x0])
    read[1]&=0b11
    read[1]=read[1]<<8
    final=read[2]
    final+=read[1]
    #print(str(final))
    time.sleep(0.25)
    return final


try:
    camera = KibbleKounter.setupCamera()
    fname= KibbleKounter.takePicture(camera,'picture1')
    print (fname) 
except Exception:
    traceback.print_exc()

try:
   while True:
    dist = measureDistance()
    print("Measured Distance = %.1f cm" % dist)
    time.sleep(1)
except Exception:
    traceback.print_exc()


try:
    spi=spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 100000
    spi.mode=0b00

    input("Make sure the scale has no weight, then press enter") 
    KibbleKounter.zeroScale() 
    input("Place 100g test weight on scale, then press enter") 
    KibbleKounter.TestScale() 
    while True:
        print("Scale reading "+str(KibbleKounter.readScale_grams())+ " grams")
        print("Adc reading "+str(Adc_read(spi)))
        time.sleep(0.5)
except Exception:
    traceback.print_exc()



