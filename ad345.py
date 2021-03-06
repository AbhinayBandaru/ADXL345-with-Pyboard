from machine import SPI
from pyb import Pin

READWRITE_CMD = const(0x80) 
MULTIPLEBYTE_CMD = const(0x40)
DEVID_ADDR = const(0x00)
DATAX1_ADDR = const(0x33)
DATAY1_ADDR = const(0x35)
DATAZ1_ADDR = const(0x37)

ADXL345_DEVID_VAL = const(0xe5)
ADXL345_POWER_CTL_ADDR = const(0x2D)
ADXL345_BW_RATE_ADDR = const(0x2C)
ADXL345_DATA_FORMAT_ADDR = const(0x31)
ADXL345_ENABLE_MSRM_ADDR = const(0x2d)
# Configuration for 100Hz sampling rate, +-2g range
ADXL345_POWER_CTL_CONF = const(0x08)
ADXL345_BW_RATE_CONF = const(0b1111)
ADXL345_DATA_FORMAT_CONF = const(0x10)
ADXL345_ENABLE_MSRM_CONF = const(0x08)

class AD345:
    def __init__(self):
        self.cs_pin = Pin('X5', Pin.OUT_PP, Pin.PULL_NONE)
        self.cs_pin.high()
        self.spi = SPI(1, SPI.MASTER, baudrate=2000000, polarity=0, phase=1, bits=8)

        self.devid = self.read_id()

        if self.devid == ADXL345_DEVID_VAL:
            self.write_bytes(ADXL345_POWER_CTL_ADDR, bytearray([ADXL345_POWER_CTL_CONF]))
            self.write_bytes(ADXL345_BW_RATE_ADDR, bytearray([ADXL345_BW_RATE_CONF]))
            self.write_bytes(ADXL345_DATA_FORMAT_ADDR, bytearray([ADXL345_DATA_FORMAT_CONF]))
            self.write_bytes(ADXL345_ENABLE_MSRM_ADDR, bytearray([ADXL345_ENABLE_MSRM_CONF]))
            self.sensitivity = 32
        else:
            raise Exception('ADXL345 accelerometer not present')

    def convert_raw_to_g(self, x):
        if x & 0x80:
            
        return x * self.sensitivity / 1000

    def read_bytes(self, addr, nbytes):
        if nbytes > 1:
            addr |= READWRITE_CMD | MULTIPLEBYTE_CMD
        else:
            addr |= READWRITE_CMD
        self.cs_pin.low()
        self.spi.send(addr)
        #buf = self.spi.send_recv(bytearray(nbytes * [0])) # read data, MSB first
        buf = self.spi.recv(nbytes)
        self.cs_pin.high()
        return buf

    def write_bytes(self, addr, buf):
        if len(buf) > 1:
            addr |= MULTIPLEBYTE_CMD
        self.cs_pin.low()
        self.spi.send(addr)
        for b in buf:
            self.spi.send(b)
        self.cs_pin.high()

    def read_id(self):
        return self.read_bytes(DEVID_ADDR, 1)[0]

    def x(self):
        return self.convert_raw_to_g(self.read_bytes(DATAX1_ADDR, 1)[0])

    def y(self):
        return self.convert_raw_to_g(self.read_bytes(DATAY1_ADDR, 1)[0])

    def z(self):
        return self.convert_raw_to_g(self.read_bytes(DATAZ1_ADDR, 1)[0])

    def xyz(self):
        return (self.x(), self.y(), self.z())
