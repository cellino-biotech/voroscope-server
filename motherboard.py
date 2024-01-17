from serial import Serial
from serial.tools import list_ports as ports
from serial.serialutil import SerialException


class SKRPico(Serial):
    """Generic RS232 serial connection"""

    def __init__(self, port: str, baudrate: int = 115200, timeout: float | None = None):
        super().__init__(port=port, baudrate=baudrate, timeout=timeout)

    @staticmethod
    def get_port_descriptions() -> list[str]:
        return [com.description for com in ports.comports()]

    @staticmethod
    def get_port_from_description(description: str) -> str:
        try:
            return [
                com.device for com in ports.comports() if description in com.description
            ][0]
        except IndexError:
            raise SerialException(f"Cannot find comport with description {description}")

    def reset_buffers(self) -> None:
        """Reset rx and tx buffers"""
        self.reset_input_buffer()
        self.reset_output_buffer()

    def send(self, msg: str, encoding: str = "utf-8") -> None:
        """Send bytearray to device"""
        self.write(f"{msg}\n".encode(encoding))
        # self.flush()

    def recv(self, encoding: str = "utf-8") -> str:
        """Receive bytearray from device"""
        return self.readline().decode(encoding).strip()
