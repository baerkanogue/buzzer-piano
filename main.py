from pyqt.qt import Window, RuntimeData
from game.game import Game
from colorama import Fore
import pygame as pg
import struct

import serial


def main():
    launcher: Window = Window()
    runtime_data: RuntimeData = launcher.run()

    mcu_port: str = runtime_data.mcu_port
    try:
        serial_port: serial.Serial = serial.Serial(mcu_port, 115200, timeout=1)
    except serial.SerialException as error:
        print(f"{Fore.RED}Invalid MCU port: {error}")
        return

    game: Game = Game(octaves_to_diplay=runtime_data.octaves)
    while game.is_running:
        played_frequency: float = game.run()
        packed_data = struct.pack("<f", played_frequency)
        serial_port.write(packed_data)
        print(played_frequency)
    pg.quit()


if __name__ == "__main__":
    print(f"{Fore.GREEN}Starting buzzer piano!{Fore.RESET}")
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.BLUE}\nKeyboard Interrupt...{Fore.RESET}")
    print(f"{Fore.GREEN}Goodbye buzzer piano!{Fore.RESET}")
