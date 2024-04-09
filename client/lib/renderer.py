import pygame
import math
from pygame import Surface
from pygame.locals import *
from enum import Enum, auto
from collections.abc import Callable


class ScaleMode(Enum):
    PIXEL_PERFECT = auto()
    FIT = auto()
    STRETCH = auto()

    def next(self):
        members = list(ScaleMode)
        return members[(members.index(self) + 1) % len(members)]


class Renderer:
    def __init__(self, window_size: tuple[int, int], resize_handler: Callable[[tuple[int, int]], tuple[int, int]], canvas_color: str = "black", bg_color: str = "black"):
        self._canvas_color = canvas_color
        self._bg_color = bg_color
        self._resize_handler = resize_handler
        self._surface_size = None
        self._surface_dirty = True
        self._viewport_dirty = True
        self._scale_mode = ScaleMode.PIXEL_PERFECT
        self._update_size(window_size)

    @property
    def surface(self) -> Surface:
        if self._surface_dirty:
            self._update_surface()
        return self._surface

    @property
    def scale_mode(self) -> ScaleMode:
        return self._scale_mode

    @scale_mode.setter
    def scale_mode(self, v: ScaleMode):
        self._scale_mode = v
        self._viewport_dirty = True

    def render(self, alpha: float = 1):
        for event in pygame.event.get(VIDEORESIZE):
            self._update_size(event.size)

        if self._surface_dirty:
            self._update_surface()

        if self._viewport_dirty:
            self._update_viewport()

        ts = self._surface
        if self._surface_size != self._viewport:
            ts = pygame.transform.smoothscale(self._surface, self._viewport)

        if alpha < 1:
            ts.set_alpha(int(alpha * 255))

        self._screen.fill(self._bg_color)
        self._screen.blit(ts, self._viewpoint)
        self._surface.fill(self._canvas_color)
        pygame.display.flip()

    def invalidate_surface_size(self):
        self._surface_dirty = True

    def get_mouse(self) -> tuple[int, int]:
        if self._viewport_dirty:
            self._update_viewport()
        ps = pygame.mouse.get_pos()
        ps = (round((ps[0] - self._viewpoint[0]) * self._surface_size[0] / self._viewport[0]),
              round((ps[1] - self._viewpoint[1]) * self._surface_size[1] / self._viewport[1]))
        return ps

    def _update_viewport(self):
        win_size = self._screen.get_size()
        if self._scale_mode == ScaleMode.STRETCH:
            self._viewport = win_size
        else:
            csize = self._surface_size
            scale = min(win_size[0] / csize[0], win_size[1] / csize[1])
            if self._scale_mode == ScaleMode.PIXEL_PERFECT:
                scale = int(scale) if scale >= 1 else 1 / math.ceil(1 / scale)
            self._viewport = (int(csize[0] * scale), int(csize[1] * scale))

        self._viewpoint = ((win_size[0] - self._viewport[0]) // 2, (win_size[1] - self._viewport[1]) // 2)
        self._viewport_dirty = False

    def _update_surface(self):
        allowed_size = self._resize_handler(self._screen.get_size())
        if self._surface_size != allowed_size:
            self._surface_size = allowed_size
            self._surface = Surface(allowed_size)
            self._surface.fill(self._canvas_color)
            self._viewport_dirty = True
        self._surface_dirty = False

    def _update_size(self, window_size: tuple[int, int]):
        self._screen = pygame.display.set_mode(window_size, RESIZABLE)
        self._surface_dirty = True
        self._viewport_dirty = True
