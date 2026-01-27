import pygame as pg
from pygame.math import Vector2
from pathlib import Path
from helpers import *
from typing import Any
from dataclasses import dataclass


class Key:
    white_key_path: Path = Path("assets", "white.png")
    black_key_path: Path = Path("assets", "black.png")
    white_key_pressed_path: Path = Path("assets", "white_pressed.png")
    black_key_pressed_path: Path = Path("assets", "black_pressed.png")

    white_key: pg.Surface = pg.image.load(white_key_path)
    black_key: pg.Surface = pg.image.load(black_key_path)
    white_key_pressed: pg.Surface = pg.image.load(white_key_pressed_path)
    black_key_pressed: pg.Surface = pg.image.load(black_key_pressed_path)

    white_keys_padding_pixels: int = 4
    white_key_full_width: int = white_key.get_width() + white_keys_padding_pixels
    black_width: int = black_key.get_width()

    white_notes = ("do", "re", "mi", "fa", "sol", "la", "si")
    black_notes = ("do#", "fa#", "fa#", "sol#", "la#")

    def __init__(self, is_white: bool) -> None:
        self.is_white: bool = is_white
        self.is_pressed: bool = False
        self.hitbox: pg.Rect = self.get_sprite().get_rect()
        self.position: Vector2
        self.note: str

    def get_sprite(self) -> pg.Surface:
        if self.is_white:
            if self.is_pressed:
                return self.white_key_pressed
            else:
                return self.white_key
        else:
            if self.is_pressed:
                return self.black_key_pressed
            else:
                return self.black_key

    def sync_hitbox(self) -> None:
        self.hitbox.topleft = (int(self.position.x), int(self.position.y))

    @classmethod
    def convert_alpha(cls) -> None:
        cls.white_key.convert_alpha()
        cls.black_key.convert_alpha()

        cls.white_key_pressed.convert_alpha()
        cls.black_key_pressed.convert_alpha()


@dataclass(frozen=True)
class RuntimeContext:
    window_size: Vector2
    max_fps: int
    clock: pg.time.Clock
    screen: pg.Surface


class Game:
    def __init__(self) -> None:
        self.note_played: str = ""

    def main(self) -> None:
        pg.init()
        pg.display.set_caption("Buzzer Piano")
        OCTAVES_TO_DISPLAY: int = 3
        screen: pg.Surface = self.init_screen(OCTAVES_TO_DISPLAY)

        max_fps: int = 120
        clock: pg.time.Clock = pg.time.Clock()

        keys: list[Key] = []
        self.keyboard_display_init(OCTAVES_TO_DISPLAY, keys)
        white_keys: list[Key] = []
        black_keys: list[Key] = []
        for key in keys:
            if key.is_white:
                white_keys.append(key)
            else:
                black_keys.append(key)

        is_running: bool = True
        while is_running:
            screen.fill("black")
            event_res: dict[Any, Any] = self.event_handler()
            is_running = event_res["is_running"]

            dt: float = clock.tick(max_fps) / 1000.0

            self.get_key(white_keys, black_keys)

            self.update(keys, screen)
            self.auto_sync(keys)

    def init_screen(self, octaves_to_display: int) -> pg.Surface:
        window_size: Vector2 = Vector2(
            Key.white_key_full_width * (octaves_to_display * 7),
            Key.white_key.get_height(),
        )

        return pg.display.set_mode(window_size)

    def get_key(self, white_keys_list: list[Key], black_keys_list: list[Key]) -> None:
        mouse_position: tuple[int, int] = pg.mouse.get_pos()
        lmb_pressed: bool = pg.mouse.get_pressed()[0]

        for key in black_keys_list:
            if key.hitbox.collidepoint(mouse_position) and lmb_pressed:
                key.is_pressed = True
                print(key.note)
                return
            else:
                key.is_pressed = False

        for key in white_keys_list:
            if key.hitbox.collidepoint(mouse_position) and lmb_pressed:
                key.is_pressed = True
                print(key.note)
                return
            else:
                key.is_pressed = False

    def update(self, actors: list[Key], screen: pg.Surface) -> None:
        self.auto_blit(actors, screen)
        pg.display.update()

    def auto_blit(self, keys: list[Key], screen: pg.Surface) -> None:
        for key in keys:
            screen.blit(key.get_sprite(), key.position)

    def auto_sync(self, keys: list[Key]) -> None:
        for key in keys:
            key.sync_hitbox()

    def event_handler(self) -> dict[Any, Any]:
        res: dict[Any, Any] = {
            "is_running": True,
        }

        for event in pg.event.get():
            if event.type == pg.QUIT:
                res["is_running"] = False

        return res

    def keyboard_display_init(
        self, octaves_to_display: int, keys_list: list[Key]
    ) -> None:
        octave_layout = (
            "w",
            "b",
            "w",
            "b",
            "w",
            "w",
            "b",
            "w",
            "b",
            "w",
            "b",
            "w",
        )

        white_index: int = 0
        for octave_index in range(octaves_to_display):
            for key in octave_layout:
                match key:
                    case "w":
                        white_posx: float = Key.white_key_full_width * white_index
                        white_posy: float = 0.0

                        new_white_key: Key = Key(is_white=True)
                        new_white_key.position = Vector2(white_posx, white_posy)
                        new_white_key.note = f"{Key.white_notes[white_index % (len(Key.white_notes))]}_{octave_index}"

                        keys_list.append(new_white_key)

                        white_index += 1
                    case "b":
                        pass
        white_index: int = 0
        black_index: int = 0
        for octave_index in range(octaves_to_display):
            for key in octave_layout:
                match key:
                    case "w":
                        white_index += 1
                    case "b":
                        black_posx: float = (
                            Key.white_key_full_width * white_index
                            - (Key.black_width // 2)
                            - 2
                        )
                        black_posy: float = 0.0

                        new_black_key: Key = Key(is_white=False)
                        new_black_key.position = Vector2(black_posx, black_posy)
                        new_black_key.note = f"{Key.black_notes[black_index % (len(Key.black_notes))]}_{octave_index}"

                        keys_list.append(new_black_key)
                        black_index += 1


if __name__ == "__main__":
    color_print("green", "Starting buzzer piano!")
    try:
        Game().main()
        pg.quit()
    except KeyboardInterrupt:
        color_print("red", "\nKeyboard Interrupt...")
    color_print("green", "Goodbye buzzer piano!")
