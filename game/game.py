from path_resolver import resource_path
from dataclasses import dataclass
from pygame.math import Vector2
from colorama import Fore
from pathlib import Path
from typing import Any
import pygame as pg


class Key:
    """
    Key object holds global data for initializing a piano by defining it's keys.
    Each key instance represent a single piano key, and have an assciated note property.
    """

    white_key_path: Path = Path("game", "assets", "white.png")
    black_key_path: Path = Path("game", "assets", "black.png")
    white_key_pressed_path: Path = Path("game", "assets", "white_pressed.png")
    black_key_pressed_path: Path = Path("game", "assets", "black_pressed.png")

    white_key: pg.Surface = pg.image.load(resource_path(str(white_key_path)))
    black_key: pg.Surface = pg.image.load(resource_path(str(black_key_path)))
    white_key_pressed: pg.Surface = pg.image.load(
        resource_path(str(white_key_pressed_path))
    )
    black_key_pressed: pg.Surface = pg.image.load(
        resource_path(str(black_key_pressed_path))
    )

    white_keys_padding_pixels: int = 4
    white_key_full_width: int = white_key.get_width() + white_keys_padding_pixels
    black_width: int = black_key.get_width()

    white_notes = (32.69, 36.68, 41.2, 43.64, 48.98, 55.0, 61.73)
    black_notes = (34.62, 38.84, 46.21, 51.87, 58.24)

    def __init__(self, is_white: bool) -> None:
        self.is_white: bool = is_white
        self.is_pressed: bool = False
        self.hitbox: pg.Rect = self.get_sprite().get_rect()
        if self.is_white:
            self.hitbox = self.hitbox.inflate(self.white_keys_padding_pixels, 0.0)
        self.position: Vector2
        self.note: float

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
        """
        This need to be called everytime a piano key position is set,
        to have it's hitbox set to the new position.
        """

        self.hitbox.topleft = (int(self.position.x), int(self.position.y))

    def set_note_octave(self, frequency: float, octave: int) -> None:
        self.note = frequency * (2**octave)

    @classmethod
    def convert_alpha(cls) -> None:
        """
        This method helps for pygame initialization order problem.
        The window needs to know the size of the key sprite to be called,
        but the convert_alpha method needs the window to be initialized.
        """

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
    """
    Game holds and execute the pygame logic to run the piano app.

    :param octaves_to_display: How many octaves to display
    """

    def __init__(self, octaves_to_diplay: int) -> None:
        pg.init()
        pg.display.set_caption("Buzzer Piano")
        self.set_icon()

        self.OCTAVES_TO_DISPLAY: int = octaves_to_diplay
        self.screen: pg.Surface = self.init_screen(self.OCTAVES_TO_DISPLAY)

        self.MAX_FPS: int = 120
        self.clock: pg.time.Clock = pg.time.Clock()

        self.keys: list[Key] = []
        self.keyboard_display_init(self.OCTAVES_TO_DISPLAY, self.keys)
        self.white_keys: list[Key] = []
        self.black_keys: list[Key] = []

        for key in self.keys:
            if key.is_white:
                self.white_keys.append(key)
            else:
                self.black_keys.append(key)

        self.is_running: bool = True

    def run(self) -> float:
        """
        Main loop for the game.

        :return: Returns the note played by the piano.
        :rtype: str | None
        """
        self.screen.fill("black")
        event_res: dict[Any, Any] = self.event_handler()
        self.is_running = event_res["is_running"]

        dt: float = self.clock.tick(self.MAX_FPS) / 1000.0

        note = self.get_note(self.white_keys, self.black_keys)

        self.update(self.keys, self.screen)
        self.auto_sync(self.keys)

        return note

    def init_screen(self, octaves_to_display: int) -> pg.Surface:
        window_size: Vector2 = Vector2(
            Key.white_key_full_width * (octaves_to_display * 7),
            Key.white_key.get_height(),
        )

        return pg.display.set_mode(window_size)

    def get_note(self, white_keys_list: list[Key], black_keys_list: list[Key]) -> float:
        mouse_position: tuple[int, int] = pg.mouse.get_pos()
        lmb_pressed: bool = pg.mouse.get_pressed()[0]

        all_keys: list[Key] = white_keys_list + black_keys_list

        for key in all_keys:
            key.is_pressed = False

        for key in black_keys_list:
            if key.hitbox.collidepoint(mouse_position) and lmb_pressed:
                key.is_pressed = True
                return key.note

        for key in white_keys_list:
            if key.hitbox.collidepoint(mouse_position) and lmb_pressed:
                key.is_pressed = True
                return key.note

        return 0.0

    def update(self, keys: list[Key], screen: pg.Surface) -> None:
        """
        Update all sprites in the keys list.

        :param keys: List of all the keys objects
        :type keys: list[Key]
        :param screen: Surface object to display the keys
        :type screen: pg.Surface
        """

        for key in keys:
            screen.blit(key.get_sprite(), key.position)

        pg.display.update()

    def auto_sync(self, keys: list[Key]) -> None:
        """
        Automatically calls the sync_hitbox method of each key in keys list.

        :param keys: List of all the keys hitbox to update
        :type keys: list[Key]
        """
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
        """
        Creates the layout of the piano, by creating all the keys objects
        and populates the keys list.

        :param octaves_to_display: How many octaves will the piano have
        :type octaves_to_display: int
        :param keys_list: List of keys to populate
        :type keys_list: list[Key]
        """

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

        # all white keys need to be drawn first
        white_index: int = 0
        BASE_OCTAVE: int = 3
        for octave_index in range(octaves_to_display):
            for key in octave_layout:
                match key:
                    case "w":
                        white_posx: float = Key.white_key_full_width * white_index
                        white_posy: float = 0.0

                        new_white_key: Key = Key(is_white=True)
                        new_white_key.position = Vector2(white_posx, white_posy)
                        note_base_frequency: float = Key.white_notes[
                            white_index % len(Key.white_notes)
                        ]
                        new_white_key.set_note_octave(
                            note_base_frequency, BASE_OCTAVE + octave_index
                        )

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
                        note_base_frequency = Key.black_notes[
                            black_index % (len(Key.black_notes))
                        ]
                        new_black_key.set_note_octave(
                            note_base_frequency, BASE_OCTAVE + octave_index
                        )

                        keys_list.append(new_black_key)
                        black_index += 1

    def set_icon(self) -> None:
        icon_path: Path = Path("misc", "buzzer.icon")
        icon: pg.Surface = pg.image.load(resource_path(str(icon_path)))
        pg.display.set_icon(icon)


if __name__ == "__main__":
    print(f"{Fore.GREEN}Starting buzzer piano!{Fore.RESET}")
    try:
        game: Game = Game(octaves_to_diplay=3)
        while game.is_running:
            print(f"Playing: {game.run()}Hz")
        pg.quit()
    except KeyboardInterrupt:
        print(f"{Fore.BLUE}\nKeyboard Interrupt...{Fore.RESET}")
    print(f"{Fore.GREEN}Goodbye buzzer piano!{Fore.RESET}")
