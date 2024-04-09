import asyncio
import pygame
import storage
import time
import lib.request as request
from scene import Scene
from pygame.locals import *

MAX_FRAME_TIME = 200

pygame.init()
storage.init()
request.init()
pygame.display.set_caption("Крестики-Нолики :)")

scene = Scene()


async def main():
    scene.start()
    prev_time = time.time()

    while True:
        if pygame.event.peek(QUIT):
            pygame.quit()
            return

        for event in pygame.event.get(KEYDOWN):
            scene.keydown(event.key)

        for event in pygame.event.get(MOUSEBUTTONDOWN):
            if event.button in [1, 3]:
                scene.mousedown(event.button)

        cur_time = time.time()
        tick = min(MAX_FRAME_TIME, (cur_time - prev_time) * 1000)
        prev_time = cur_time

        scene.update(tick)

        await request.flush()
        await asyncio.sleep(0)

asyncio.run(main())
