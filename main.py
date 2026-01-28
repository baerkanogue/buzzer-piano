from game.game import Game
from colorama import Fore
import pygame as pg
import serial


def main():
    game: Game = Game(octaves_to_diplay=3)
    while game.is_running:
        print(game.run())
    pg.quit()


if __name__ == "__main__":
    print(f"{Fore.GREEN}Starting buzzer piano!{Fore.RESET}")
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.BLUE}\nKeyboard Interrupt...{Fore.RESET}")
    print(f"{Fore.GREEN}Goodbye buzzer piano!{Fore.RESET}")
