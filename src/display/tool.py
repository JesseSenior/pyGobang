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
from PIL import Image


def image_to_surface(pilImage: Image.Image) -> pygame.Surface:
    """Convert PIL Image to pygame Surface.

    Args:
        pilImage (Image.Image): PIL Image.

    Returns:
        pygame.Surface: pygame Surface.
    """
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode
    ).convert_alpha()


def surface_to_image(pygameSurface: pygame.Surface) -> Image.Image:
    """Convert pygame Surface to PIL Image.

    Args:
        pygameSurface (pygame.Surface): pygame Surface.

    Returns:
        Image.Image: PIL Image.
    """
    return Image.frombytes(
        "RGBA",
        pygameSurface.get_size(),
        pygame.image.tostring(pygameSurface, "RGBA", False),
    )

