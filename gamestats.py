import pygame
import json

class GameStats:
    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.reset_stats()
        self.game_active=False
        self.high_score=self.load_high_score()
        
    
    def reset_stats(self):
        self.ship_left=self.settings.ship_limit
        self.score=0
        self.level=1
    
    def save_high_score(self):
        with open("highscore.json","w") as f:
            json.dump(self.high_score,f)

    def load_high_score(self):
        try:
            with open("highscore.json") as f:
                return int(json.load(f))
        except (FileNotFoundError,ValueError):
            return 0
