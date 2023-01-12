"""pyGobang, a python based Gobang game.

Copyright (C) 2022 Jesse Senior

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program.  If not, see <http://www.gnu.org/licenses/>.

File: src/display/tool.py
Description: Other practical tools for the display.
"""
import pygame
import src.constants

from PIL import Image


def image_to_surface(image: Image.Image) -> pygame.Surface:
    """Convert PIL Image to pygame Surface.

    Args:
        image (Image.Image): PIL Image.

    Returns:
        pygame.Surface: pygame Surface.
    """
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode)


def surface_to_image(surface: pygame.Surface) -> Image.Image:
    """Convert pygame Surface to PIL Image.

    Args:
        surface (pygame.Surface): pygame Surface.

    Returns:
        Image.Image: PIL Image.
    """
    return Image.frombytes(
        "RGBA",
        surface.get_size(),
        pygame.image.tostring(surface, "RGBA", False),
    )
    
def play_sound(sound_path):
    if not src.constants.MUTE_SOUND:
        sound=pygame.mixer.Sound(src.constants.res_path(sound_path))
        sound.set_volume(src.constants.SOUND_VOLUME)
        sound.play()