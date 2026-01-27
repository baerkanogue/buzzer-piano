import pygame as pg
from pygame.math import Vector2
from pathlib import Path
from helpers import *
from typing import Any
from dataclasses import dataclass


class Sprite:
    image: pg.Surface
    path: str
    position: Vector2
    hitbox: pg.Rect

    def __init__(self, path: str | Path, use_alpha: bool = False) -> None:
        self.position = Vector2()
        self.path = str(path)
        self.load_image(path, use_alpha)
        self.hitbox = self.image.get_rect()

    def load_image(
        self,
        img_path: str | Path | None = None,
        use_alpha: bool = False,
    ) -> None:
        working_path: str | Path = img_path if img_path else self.path
        try:
            if not use_alpha:
                self.image = pg.image.load(
                    working_path
                ).convert()  # converts image for faster memory access
            else:
                self.image = pg.image.load(
                    working_path
                ).convert_alpha()  # use convert_alpha for alpha images
            self.hitbox = self.image.get_rect()
        except Exception as error:
            print(error)
            return

    def sync_hitbox(self) -> None:
        self.hitbox.topleft = (int(self.position.x), int(self.position.y))


@dataclass(frozen=True)
class RuntimeContext:
    window_size: Vector2
    max_fps: int
    clock: pg.time.Clock
    screen: pg.Surface


class Game:
    def main(self) -> None:
        pg.init()
        pg.display.set_caption("Buzzer Piano")
        screen: pg.Surface = pg.display.set_mode((200, 200))

        max_fps: int = 120
        clock: pg.time.Clock = pg.time.Clock()

        white_key_path: Path = Path("assets", "white.png")
        black_key_path: Path = Path("assets", "black.png")

        white_key_reference: Sprite = Sprite(white_key_path)
        black_key_reference: Sprite = Sprite(black_key_path)
        octave_layout: tuple = (
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

        octaves_to_display: int = 2
        white_keys_padding_pixels: int = 4
        key_full_width: int = (
            white_key_reference.image.get_width() + white_keys_padding_pixels
        )
        black_width: int = black_key_reference.image.get_width()

        window_size: Vector2 = Vector2(
            key_full_width * (octaves_to_display * 7),
            white_key_reference.image.get_height(),
        )
        screen: pg.Surface = pg.display.set_mode(window_size)

        actors: list[Sprite] = []

        is_running: bool = True
        while is_running:
            screen.fill("black")
            event_res: dict[Any, Any] = self.event_handler()
            is_running = event_res["is_running"]

            white_index: int = 0
            for _ in range(octaves_to_display):
                for key in octave_layout:
                    match key:
                        case "w":
                            white_posx: float = key_full_width * white_index
                            white_posy: float = 0.0

                            new_white_key: Sprite = Sprite(white_key_path, True)
                            new_white_key.position = Vector2(white_posx, white_posy)

                            actors.append(new_white_key)

                            white_index += 1
                        case "b":
                            pass
            white_index: int = 0
            for _ in range(octaves_to_display):
                for key in octave_layout:
                    match key:
                        case "w":
                            white_index += 1
                        case "b":
                            black_posx: float = (
                                key_full_width * white_index - (black_width // 2) - 2
                            )
                            black_posy: float = 0.0

                            new_black_key: Sprite = Sprite(black_key_path)
                            new_black_key.position = Vector2(black_posx, black_posy)

                            actors.append(new_black_key)

            dt: float = clock.tick(max_fps) / 1000.0

            self.update(actors, screen)

    def update(self, actors: list[Sprite], screen: pg.Surface) -> None:
        self.auto_blit(actors, screen)
        pg.display.update()

    def auto_blit(self, sprites: list[Sprite], screen: pg.Surface) -> None:
        for sprite in sprites:
            screen.blit(sprite.image, sprite.position)

    def auto_sync(self, sprites: list[Sprite]) -> None:
        for sprite in sprites:
            sprite.sync_hitbox()

    def event_handler(self) -> dict[Any, Any]:
        res: dict[Any, Any] = {
            "is_running": True,
        }

        for event in pg.event.get():
            if event.type == pg.QUIT:
                res["is_running"] = False

        return res


if __name__ == "__main__":
    color_print("green", "Starting buzzer piano!")
    try:
        Game().main()
        pg.quit()
    except KeyboardInterrupt:
        color_print("red", "\nKeyboard Interrupt...")
    color_print("green", "Goodbye buzzer piano!")
