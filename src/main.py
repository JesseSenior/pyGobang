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

File: src/main.py
Description: 
    Include the main function of the program, which is responsible for the 
    initialization of the game interface, switching, exiting and the message 
    loop.
"""
import pygame

from src.constants import WINDOW_SIZE
from src.display.screen import screen_list


def main():
    pygame.init()
    pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("pyGobang, a python based Gobang game")
    icon = pygame.image.load("res/image/icon.png").convert_alpha()
    pygame.display.set_icon(icon)
    screen_status = 1
    while screen_status != 0:
        screen_status = screen_list[screen_status]().loop()
    pygame.quit()
