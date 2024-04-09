from pygame.mixer import Sound
import os

sounds: dict[str, Sound] = {}

debug: bool = False


def init():
    # images_path = "assets/images/"
    sound_path = "assets/sounds/"
    # fonts_path = "assets/fonts/"

    for file in os.listdir(sound_path):
        name = file.split('.')[0]
        sounds[name] = Sound(sound_path + file)
