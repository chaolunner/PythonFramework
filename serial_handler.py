import serial.tools.list_ports
import threading

from events import EventHandler


class SerialHandler:
    DEFAULT_PORT = "/dev/rfcomm0"

    def __init__(self):
        self.is_running = False
        self.message = None  # type: str
        self.on_data_received = EventHandler(self)
        self.thread = None  # type: threading.Thread
        self.serial_port = None  # type: serial.Serial

    @staticmethod
    def has_port(port: str = None):
        for list_port_info in serial.tools.list_ports.comports():
            if list_port_info.device == port:
                return True
        return False

    def open(self, port=DEFAULT_PORT):
        if SerialHandler.has_port(port):
            if self.serial_port is None:
                self.serial_port = serial.Serial(port, timeout=0)
            if self.serial_port.isOpen() is False:
                self.serial_port.open()
            if self.serial_port.isOpen():
                # It is important to clear all the messages that sent and received before connection
                self.serial_port.flush()
                self.is_running = True
                if self.thread is None:
                    self.thread = threading.Thread(target=self.read)
                    self.thread.setDaemon(True)
                    self.thread.start()
        else:
            print(str.format("Can't found the {0} port!", port))

    def close(self):
        self.is_running = False

        if self.serial_port is not None and self.serial_port.isOpen():
            self.serial_port.close()

    @property
    def is_connected(self):
        return self.is_running and self.serial_port is not None and self.serial_port.isOpen()

    def read(self):
        while self.is_connected:
            try:
                self.message = self.serial_port.readline()
                if len(self.message) > 0:
                    # If this message is a packed message, you should parse it in the following way:
                    self.on_data_received(str(self.message).replace("\\\\", "\\")[2:-3])
                    # Otherwise:
                    # self.on_data_received(str(self.message))
            except Exception as e:
                print(e)

    def write(self, message: str = None):
        if self.is_connected:
            try:
                message = message.replace("\n", "").replace("\\n", "")
                if message.endswith("\n") is False:
                    message += "\n"
                self.serial_port.write(message.encode())
            except Exception as e:
                print(e)
