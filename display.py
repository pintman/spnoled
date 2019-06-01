import serial
import time
import socket

HOST_PORT = 'localhost', 5206
DEVICE = '/dev/ttyACM3'
BAUDRATE = 9600
WIDTH = 128
HEIGHT = 64
DEFAULT_OFFSET = [3000, 2000]
SEND_TO_PROCESSING = False


class Display:
    def __init__(self):
        self.buffer = []
        self.offset = DEFAULT_OFFSET
        self.width = WIDTH
        self.height = HEIGHT
        self.socket = socket.socket()
        if SEND_TO_PROCESSING:
            self.socket.connect(HOST_PORT)

        self.last_update = time.time()
        try:
            self.ser = serial.Serial(DEVICE, BAUDRATE)
        except:
            print(DEVICE, "not found. Trying default device.")
            time.sleep(1)
            self.ser = serial.Serial('/dev/ttyACM0', BAUDRATE)

    def px(self, x, y, on_off):
        if on_off:
            self.buffer.extend([ord('p'), x, y])
            #print("sending", x, y)
            #self.ser.write(b'p')
            #self.ser.write(x)
            #self.ser.write(y)
            #self.ser.write(b'\n')

    def clear(self):
        #print("Sending clear")
        self.buffer.append(ord('c'))
        #self.ser.write(b'c\n')

    def update(self):
        self.buffer.append(ord('u'))
        print("Sending buffer with ", len(self.buffer), 
              "Bytes. Since last Update", round(time.time() - self.last_update, 1))
        bytes_written = self.ser.write(self.buffer)
        if SEND_TO_PROCESSING:
            self.socket.send(bytes(self.buffer))
        self.ser.flush()
        print("Sending finished. Bytes written", bytes_written)
        self.buffer.clear()
        self.last_update = time.time()

    def test(self):
        print("Starting test program")
        while True:
            print('an')
            self.ser.write(b'0')
            #self.ser.write(b'\n')
            time.sleep(1)
            print('aus')
            self.ser.write(b'1')
            #self.ser.write(b'\n')
            time.sleep(1)

if __name__ == '__main__':
    disp = Display()
    disp.test()
