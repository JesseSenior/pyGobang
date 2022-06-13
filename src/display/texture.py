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

File: src/display/texture.py
Description: Generate texture from small texture.
"""
import pygame
import numpy as np
import heapq
from random import choice
from math import ceil
from typing import Tuple
from PIL import Image
from skimage import util

import src.constants
from src.constants import OVERLAY_SCALE, TEXTURE_BLOCK_SIZE
from src.display.tool import image_to_surface


def L2_overlay_diff(patch, block_size, overlap, res, y, x):
    error = 0
    if x > 0:
        left = patch[:, :overlap] - res[y : y + block_size, x : x + overlap]
        error += np.sum(left ** 2)

    if y > 0:
        up = patch[:overlap, :] - res[y : y + overlap, x : x + block_size]
        error += np.sum(up ** 2)

    if x > 0 and y > 0:
        corner = (
            patch[:overlap, :overlap] - res[y : y + overlap, x : x + overlap]
        )
        error -= np.sum(corner ** 2)

    return error


def random_patch(texture, block_size):
    h, w, _ = texture.shape
    i = np.random.randint(h - block_size)
    j = np.random.randint(w - block_size)

    return texture[i : i + block_size, j : j + block_size]


def random_best_patch(texture, block_size, overlap, res, y, x):
    h, w, _ = texture.shape
    errors = np.full((h - block_size, w - block_size), np.inf)

    for t in range(src.constants.SELECT_ATTEMPT):
        i, j = choice(range(h - block_size)), choice(range(w - block_size))
        patch = texture[i : i + block_size, j : j + block_size]
        e = L2_overlay_diff(patch, block_size, overlap, res, y, x)
        errors[i, j] = e

    i, j = np.unravel_index(np.argmin(errors), errors.shape)
    return texture[i : i + block_size, j : j + block_size]


def min_cut_path(errors):
    # dijkstra's algorithm vertical
    pq = [(error, [i]) for i, error in enumerate(errors[0])]
    heapq.heapify(pq)

    h, w = errors.shape
    seen = set()

    while pq:
        error, path = heapq.heappop(pq)
        curDepth = len(path)
        curIndex = path[-1]

        if curDepth == h:
            return path

        for delta in -1, 0, 1:
            nextIndex = curIndex + delta

            if 0 <= nextIndex < w:
                if (curDepth, nextIndex) not in seen:
                    cumError = error + errors[curDepth, nextIndex]
                    heapq.heappush(pq, (cumError, path + [nextIndex]))
                    seen.add((curDepth, nextIndex))


def min_cut_patch(patch, block_size, overlap, res, y, x):
    patch = patch.copy()
    dy, dx, _ = patch.shape
    minCut = np.zeros_like(patch, dtype=bool)

    if x > 0:
        left = patch[:, :overlap] - res[y : y + dy, x : x + overlap]
        leftL2 = np.sum(left ** 2, axis=2)
        for i, j in enumerate(min_cut_path(leftL2)):
            minCut[i, :j] = True

    if y > 0:
        up = patch[:overlap, :] - res[y : y + overlap, x : x + dx]
        upL2 = np.sum(up ** 2, axis=2)
        for j, i in enumerate(min_cut_path(upL2.T)):
            minCut[:i, j] = True

    np.copyto(patch, res[y : y + dy, x : x + dx], where=minCut)

    return patch


def quilt(texture: Image.Image, block_size, num_block):
    texture = util.img_as_float(texture)

    overlap = block_size // OVERLAY_SCALE
    num_blockHigh, num_blockWide = num_block

    h = (num_blockHigh * block_size) - (num_blockHigh - 1) * overlap
    w = (num_blockWide * block_size) - (num_blockWide - 1) * overlap

    res = np.zeros((h, w, texture.shape[2]))

    for i in range(num_blockHigh):
        for j in range(num_blockWide):
            y = i * (block_size - overlap)
            x = j * (block_size - overlap)

            if i == 0 and j == 0:
                patch = random_patch(texture, block_size)
            else:
                patch = random_best_patch(
                    texture, block_size, overlap, res, y, x
                )
                patch = min_cut_patch(patch, block_size, overlap, res, y, x)

            res[y : y + block_size, x : x + block_size] = patch

    image = Image.fromarray((res * 255).astype(np.uint8))
    return image


def generate_texture(
    texture_path: str, size: Tuple[int, int]
) -> pygame.Surface:
    """Generate texture from small texture.

    Args:
        texture_path (str): Path to the small texture.
        size (Tuple[int, int]): The required size.

    Returns:
        pygame.Surface: Surface with the generated texture.
    """
    texture = Image.open(texture_path)
    block_size = min(TEXTURE_BLOCK_SIZE, *texture.size)
    num_block = (
        ceil(size[1] / (block_size - block_size // OVERLAY_SCALE)),
        ceil(size[0] / (block_size - block_size // OVERLAY_SCALE)),
    )
    extended_texture = pygame.Surface(size)
    extended_texture.blit(
        image_to_surface(quilt(texture, block_size, num_block)), (0, 0)
    )
    return extended_texture
