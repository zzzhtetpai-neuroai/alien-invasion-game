import pygame.font
from ship import Ship
from pygame.sprite import Group

class ScoreBoard:
    def __init__(self,ai_game):
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.settings=ai_game.settings
        self.stats=ai_game.stats
        self.text_color=(0,0,0)
        self.font=pygame.font.SysFont(None,48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # score_str=str(self.stats.score)
        self.screen_rect=self.screen.get_rect()
        round_score=round(self.stats.score,-1)  # this changes the int into str
        score_str="Score"+" "+"{:,}".format(round_score)
        self.score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20
    
    def prep_high_score(self):
        high_score=round(self.stats.high_score,-1)
        high_score_str="High Score"+" "+"{:,}".format(high_score)
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.center=self.screen_rect.center
        self.high_score_rect.top=self.score_rect.top
    
    def prep_level(self):
        lvl_str="Level"+" "+str(self.stats.level)
        self.lvl_image=self.font.render(lvl_str,True,self.text_color,self.settings.bg_color)
        self.lvl_rect=self.lvl_image.get_rect()
        self.lvl_rect.right=self.score_rect.right
        self.lvl_rect.top=self.score_rect.bottom+10
    
    def prep_ships(self):
        self.ships=Group()
        for ship_number in range(self.stats.ship_left):
            ship=Ship(self.ai_game)      # Here Ship() needs one argument class but u cant type ai_game here because here it needs an actual class not a define method passing class to a function
            ship.image=pygame.transform.scale(ship.image,(40,40))
            ship.rect.x=10+ship.rect.width*ship_number
            ship.rect.top=10   # here it equals to self.rect.y becuz we are not comparing top or bottom
            self.ships.add(ship)

    def check_high_score(self):
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score
            # self.stats.save_high_score
            self.prep_high_score()


    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.lvl_image,self.lvl_rect)
        self.ships.draw(self.screen)

        # self.screen.blit(self.ai_game.ship.image,self.ai_game.ship.rect)

    
