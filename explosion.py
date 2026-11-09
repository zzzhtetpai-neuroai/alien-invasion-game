import pygame
import os
from pygame.sprite import Sprite

class Explosion(Sprite):
    def __init__(self, ai_game, position):
        super().__init__()
        self.screen = ai_game.screen

        # Load all explosion frames into a list
        self.frames = []
        self._load_frames()

        # Start with the first frame
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=position)

        # Control animation speed
        self.frame_rate = 18  # Lower = faster animation
        self.counter = 0

    def _load_frames(self):
        folder_path = "Images/explosion_frames"
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                frame = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                self.frames.append(frame)

    def update(self):
        self.counter += 1
        if self.counter % self.frame_rate == 0:
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()  # Remove explosion sprite when animation ends

    def draw(self):
        self.screen.blit(self.image, self.rect)