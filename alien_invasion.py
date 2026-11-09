import sys   
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from gamestats import GameStats
from button import Button
from scoreboard import ScoreBoard
from explosion import Explosion

class AlienInvasion:
    def __init__(self):
       pygame.init() 
       self.settings=Settings()   
       self.screen=pygame.display.set_mode((1200,800),pygame.RESIZABLE)
       self.settings.screen_width=self.screen.get_rect().width
       self.settings.screen_height=self.screen.get_rect().height
       self.bg_image=pygame.image.load("Images/galaxy.jpg")
       self.bg_image=pygame.transform.scale(self.bg_image,(self.settings.screen_width,self.settings.screen_height))
       pygame.display.set_caption("Alien Invasion")
       self.stats=GameStats(self)
       self.sb=ScoreBoard(self)
       self.ship=Ship(self)
       self.bullets=pygame.sprite.Group()
       self.aliens=pygame.sprite.Group()
       self._create_fleet()
       self.play_button=Button(self,"Play")
       self.bullet_sound=pygame.mixer.Sound("Sounds/bullet.wav")
       self.hit_sound=pygame.mixer.Sound("Sounds/explosion.wav")
       self.bullet_sound.set_volume(0.5)
       self.hit_sound.set_volume(0.8)
       self.explosions = pygame.sprite.Group()    #%%%%
       

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self._update_aliens()
                self.explosions.update()
            self._update_screen()
            
        
           
    def _check_events(self):
        for event in pygame.event.get( ):   
                if event.type == pygame.QUIT:
                    self.stats.save_high_score()  ## my code
                    sys.exit()

                elif event.type==pygame.KEYDOWN:
                    self._check_keydown_events(event)           #enter (event) again or the game quit

                elif event.type==pygame.KEYUP:
                       self._check_keyup_events(event)
                
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                elif event.type==pygame.VIDEORESIZE:
                    self._check_screensize(event)
    
    def _check_play_button(self,mouse_pos):
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # self.stats.load_high_score()   ## my code
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)


                    
    def _update_screen(self):
        self.screen.blit(self.bg_image,(0,0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for explosion in self.explosions.sprites():
            explosion.draw()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip() 

    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        if event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        if event.key==pygame.K_ESCAPE:
            sys.exit()
        if event.key==pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
            
               
    
    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False   #u must use assignment operator (=) not the comparison one(==)
        if event.key==pygame.K_LEFT:
            self.ship.moving_left=False
    
    def _fire_bullet(self):
        # if len(self.bullets)<self.settings.bullet_allowed:
            channel=pygame.mixer.find_channel()
            if channel:
                channel.play(self.bullet_sound)
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom < 0:
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
    
    def _check_bullet_alien_collision(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for bullet, aliens_hit in collisions.items():
                for alien in aliens_hit:
                    explosion = Explosion(self, alien.rect.center)
                    self.explosions.add(explosion)
            channel=pygame.mixer.find_channel()
            if channel:
                channel.play(self.hit_sound)
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
                self.sb.prep_score()  #
                self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level+=1
            self.sb.prep_level()



    def _create_fleet(self):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width-(2*alien_width)
        number_aliens=available_space_x//(2*alien_width)
        available_space_y=(self.settings.screen_height -
                           (3*alien_height)-self.ship.rect.height)
        number_rows=available_space_y//(2*alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens):
                self._create_alien(alien_number,row_number)


    def _create_alien(self,alien_number,row_number):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.rect.x=alien_width+2*alien_width*alien_number
        alien.rect.y=alien_height+2*alien_height*row_number
        alien.x=float(alien.rect.x)
        self.aliens.add(alien)
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):   #takes two arguments a sprite and a group
            self.ship_hit()
        self._check_alien_bottom()
        
        
            

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break    #to avoid doing unnecessary work

    def ship_hit(self):
        if self.stats.ship_left>0:
            self.hit_sound.play()
            self.stats.ship_left-=1
            self.sb.prep_ships()
            # print(self.stats.ship_left)
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self.ship_hit()
                break
    
    def _check_screensize(self,event):
        self.screen=pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
        self.settings.screen_width=event.w
        self.settings.screen_height=event.h
        self.bg_image=pygame.image.load("Images/galaxy.jpg")
        self.bg_image=pygame.transform.scale(self.bg_image,(self.settings.screen_width,self.settings.screen_height))
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_level()
        self.sb.prep_ships()





          

        
if __name__=="__main__":  
    ai=AlienInvasion()    
    ai.run_game()     