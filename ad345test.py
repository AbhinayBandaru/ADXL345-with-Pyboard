import pyb
from ad345 import AD345
spi = pyb.SPI(X, SPI.MASTER)
spi.init(pyb.SPI.MASTER, baudrate=2000000, polarity=1, phase=0)

ad = AD345(spi)
print("SENSOR ID: %s" % (hex(ad.read_id())))

while True:
    print("ACCELEROMETER Readings: %s %s %s" % % % (ad.xyz()))  
