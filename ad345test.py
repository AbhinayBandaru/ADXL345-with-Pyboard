import pyb
from ad345 import AD345

blue = pyb.LED(1)
switch = pyb.Switch()

spi = pyb.SPI(X, SPI.MASTER)
spi.init(pyb.SPI.MASTER, baudrate=2000000, polarity=1, phase=0)

ad = AD345(spi)

print("SENSOR ID: %s" % (hex(ad.read_id())))

while True:
    
    pyb.wfi()
    
    if switch():
        pyb.delay(200)
        blue.on()
        log = open('/sd/log.csv', 'w')
        while not switch():
            t = pyb.millis()
            x, y, z = ad.xyz()
            log.write('{},{},{},{}\n'.format(t,x,y,z))
        log.close()
        blue.off()
        pyb.delay(200)
    
