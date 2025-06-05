import serial
import struct

class SDS011:
    def __init__(self, port="/dev/serial0"):
        self.ser = serial.Serial(port=port, baudrate=9600, timeout=2)
        self.ser.flushInput()

    def read(self):
        while True:
            byte = self.ser.read(size=1)
            if byte == b"\xaa":
                d = self.ser.read(size=9)
                if len(d) == 9 and d[0] == 0xc0 and d[-1] == 0xab:
                    pm25 = (d[1] + d[2]*256) / 10.0
                    pm10 = (d[3] + d[4]*256) / 10.0
                    return (pm25, pm10)

    def close(self):
        self.ser.close()
