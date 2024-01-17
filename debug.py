import sys
import time

from serial.serialutil import SerialException
from threading import Thread
from motherboard import SKRPico


def get_response(board: SKRPico) -> None:
    global TERMINATE
    while not TERMINATE:
        try:
            response = board.recv()

            if response:
                print(f"<< {response}")
        except (TypeError, SerialException):
            pass


if __name__ == "__main__":
    try:
        port = SKRPico.get_port_from_description("Pico")
        pico = SKRPico(port)
    except SerialException as err:
        if "PermissionError" in str(err):
            print("Serial port open in another program!")
            sys.exit()
        else:
            raise

    print(
        "Welcome to the serial debug program. Enter \"q\" to quit."
    )

    TERMINATE = False  # Thread killer

    t = Thread(target=get_response, args=(pico,))
    t.start()

    while True:
        try:
            cin = input(">> ")

            if cin != "q":
                pico.send(cin) if cin else None
                time.sleep(0.2)
            else:
                break
        except KeyboardInterrupt:
            break
    # NOTE: Do not use sys.exit() to close program
    # This may prematurely close thread
    # Instead, break loop and allow graceful shutdown
    TERMINATE = True
    pico.close()
