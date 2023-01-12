"""pyGobang, a python based Gobang game.

Copyright (C) 2022 Jesse Senior

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.

File: src/constants.py
Description: Constant variables for the game.
"""
from math import floor
import pygame
import pygame.freetype

WINDOW_SIZE = (800, 600)  # (WIDTH,HEIGHT)
MAX_FPS = 60
DEFAULT_BOARD_SIZE = (15, 15)  # (WIDTH,LENGTH)
MAINSCREEN_BOARD_SIZE = (13, 13)  # (WIDTH,LENGTH)

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

MUTE_SOUND = False
SOUND_VOLUME = 1.0

BLINK_PERIOD = 60 / 110  # BPM of the sound

EFFECT_DURATION_TINY = BLINK_PERIOD / 4  # Switch Status
EFFECT_DURATION_MINI = BLINK_PERIOD / 2  # Screen Change
EFFECT_DURATION_NORMAL = BLINK_PERIOD  # Common Widget
EFFECT_DURATION_LARGE = BLINK_PERIOD * 2  # Environment Effect
EFFECT_DURATION_HUGE = BLINK_PERIOD * 4  # Environment Effect (Long Period)

COLOR_BACKGROUND = (148, 87, 59)
COLOR_BOARD = (237, 177, 64)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (230, 230, 230)
COLOR_TRANSPARENT = (0, 0, 0, 0)

GAME_BACKGROUND = None
TEXTURE_BLOCK_SIZE = 256
SELECT_ATTEMPT = 128
OVERLAY_SCALE = 8

import os

RESPATH = os.getenv("PYGOBANG_RESPATH")


def res_path(path):
    return os.path.join(RESPATH, path)


pygame.freetype.init()
TEXT_FONT = pygame.freetype.Font(
    res_path("font/sarasa-mono-sc-nerd/sarasa-mono-sc-nerd-regular.ttf"),
    floor(min(WINDOW_SIZE) / 100 * 5),
)

SCREEN_CHANGE = pygame.event.custom_type()
TIMER_TICK = pygame.event.custom_type()
LAST_BOARD = None

DEFAULT_DATABASE_PATH = "data.db"
DATABASE_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS board_table(
   timestamp_ TEXT  PRIMARY KEY,
   competitor_black TEXT,
   competitor_white TEXT,
   board_size BLOB NOT NULL,
   kifu BLOB NOT NULL,
   winner INTEGER
) WITHOUT ROWID;
"""
DATABASE_INSERT_BOARD = """
INSERT INTO board_table 
(
    timestamp_,competitor_black,
    competitor_white,board_size,
    kifu,winner
) VALUES (?, ?, ?, ?, ?, ?)
"""
DATABASE_SELECT_BOARD = """
SELECT timestamp_,competitor_black,
       competitor_white,board_size,
       kifu,winner from board_table
"""
DATABASE_DELETE_BOARD = """
DELETE from board_table where timestamp_=?
"""

from src.database import BoardDatabase

DATABASE = BoardDatabase()
