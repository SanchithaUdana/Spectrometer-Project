import serial


class ArduinoCommunicator:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.ser = None
        self.port = port
        self.baudrate = baudrate

    def connect_to_arduino(self):
        try:
            self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=1)
            print(f'Connected to {self.port}')
            return True
        except Exception as e:
            print(f'Connection failed: {str(e)}')
            return False

    def send_request(self):
        """Send a request to the Arduino to start sending data."""
        if self.ser:
            self.ser.write(b'r')

    def read_data(self):
        """Read data from the Arduino."""
        if self.ser:
            data_list = []
            while True:
                line = self.ser.readline().decode().strip()
                if not line:
                    continue
                elif line == 's':
                    continue
                elif line == 'f':
                    break
                else:
                    data_list.append(int(line))

            if data_list:
                data_list.pop()

            return data_list
        return None
