from game.game import Game
from colorama import Fore
import pygame as pg
import struct


def main():
    while True:
        try:
            octaves = int(input("How many octaves: "))
            break
        except ValueError as error:
            print(f"Error: {error}")

    game: Game = Game(octaves_to_diplay=octaves)
    print(f"{Fore.GREEN}Ready to send data...{Fore.RESET}")
    while game.is_running:
        played_frequency: float = game.run()
        packed_data = struct.pack("<f", played_frequency)
        print(f"{played_frequency}, {packed_data}")
    pg.quit()


if __name__ == "__main__":
    print(f"{Fore.GREEN}Starting buzzer piano!{Fore.RESET}")
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.BLUE}\nKeyboard Interrupt...{Fore.RESET}")
    print(f"{Fore.GREEN}Goodbye buzzer piano!{Fore.RESET}")
