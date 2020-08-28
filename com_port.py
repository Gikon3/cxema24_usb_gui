import serial


class ComPort:
    def __init__(self, portname="COM11", baundrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE, timeout=1):
        self.PORTNAME = portname
        self.BAUNDRATE = baundrate
        self.BYTESIZE = bytesize
        self.PARITY = parity
        self.STOPBITS = stopbits
        self.TIMEOUT = timeout

        self.port = serial.Serial(
            port=self.PORTNAME,
            baudrate=self.BAUNDRATE,
            bytesize=self.BYTESIZE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            timeout=self.TIMEOUT)

        print(self.PORTNAME, "is Open")

    def flush_input_buffer(self):
        self.port.reset_input_buffer()

    def flush_output_buffer(self):
        self.port.reset_output_buffer()

    def read(self):
        line = ""
        while line[-1:] != '\0':
            byte = self.port.read(1)
            line += byte.decode('utf-8')
        return line[:-1]

    def write(self, data):
        self.port.write(data.encode('utf-8'))
