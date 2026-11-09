import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__() 
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings
        self.image=pygame.image.load('Images//ship.png')
        self.image=pygame.transform.scale(self.image,(80,120))
        self.rect=self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        self.moving_right=False     #flag
        self.moving_left=False

    def blitme(self):
        self.screen.blit(self.image,self.rect)
    
    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>0: #  # Here we have to use 'if' to make the ship stop when both keys are held down or instead if we use 'elif' it will only go right when both keys are held down
            self.x-=self.settings.ship_speed
        self.rect.x=self.x

    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        
