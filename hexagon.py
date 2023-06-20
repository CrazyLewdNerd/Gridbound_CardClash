# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 14:07:18 2022

@author: richa

MIT License

Copyright (c) 2021 Richard Baltrusch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List
from typing import Tuple
import pygame.gfxdraw
import pygame

DEFAULT_ANGLE = 0
@dataclass
class HexagonTile:
    """Hexagon class"""

    radius: float
    position: Tuple[float, float]
    colour: Tuple[int, ...]
    highlight_offset: int = 3
    max_highlight_ticks: int = 15
    id: str = ""

    def __post_init__(self):
        self.vertices = self.compute_vertices()
        self.highlight_tick = 0

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1

    def compute_vertices(self, angle=DEFAULT_ANGLE) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        self.vertices = [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]
        # Calculate rotation angle in radians
        angle = math.radians(angle)

        # Apply rotation to each vertex
        rotated_vertices = []
        for vertex in self.vertices:
            x, y = vertex
            rotated_x = (x - self.position[0]) * math.cos(angle) - (y - self.position[1]) * math.sin(angle) + \
                        self.position[0]
            rotated_y = (x - self.position[0]) * math.sin(angle) + (y - self.position[1]) * math.cos(angle) + \
                        self.position[1]
            rotated_vertices.append((rotated_x, rotated_y))
        self.vertices = rotated_vertices
        return rotated_vertices


    def compute_neighbours(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Returns hexagons whose centres are two minimal radiuses away from self.centre"""
        # could cache results for performance
        return [hexagon for hexagon in hexagons if self.is_neighbour(hexagon)]

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def render(self, screen, transparent=256*2/3, display_id=False) -> None:
        """Renders the hexagon on the screen"""
        color_with_opacity = self.colour + (transparent,)  # Add alpha value for semi-transparent
        pygame.gfxdraw.filled_polygon(screen, self.vertices, color_with_opacity)

        if display_id:
            font = pygame.font.Font(None, 20)
            id_text = font.render(self.id, True, (0, 0, 0))
            text_rect = id_text.get_rect()
            text_rect.center = (self.position[0], self.position[1] + 2 * self.minimal_radius)
            screen.blit(id_text, text_rect)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        self.highlight_tick = self.max_highlight_ticks
        # pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Colour of the hexagon tile when rendering highlight"""
        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)


class FlatTopHexagonTile(HexagonTile):
    def compute_vertices(self, angle=DEFAULT_ANGLE) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        self.vertices = [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius, y),
        ]
        # Calculate rotation angle in radians
        angle = math.radians(angle)

        # Apply rotation to each vertex
        rotated_vertices = []
        for vertex in self.vertices:
            x, y = vertex
            rotated_x = (x - self.position[0]) * math.cos(angle) - (y - self.position[1]) * math.sin(angle) + \
                        self.position[0]
            rotated_y = (x - self.position[0]) * math.sin(angle) + (y - self.position[1]) * math.cos(angle) + \
                        self.position[1]
            rotated_vertices.append((rotated_x, rotated_y))
        self.vertices = rotated_vertices
        return rotated_vertices

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x + self.radius / 2, y + self.minimal_radius)