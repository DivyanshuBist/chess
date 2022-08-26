import pygame
class Sound:
    def capture_sound(self):
        sound=pygame.mixer.Sound("../assets/sounds/capture.wav")
        pygame.mixer.Sound.play(sound)
    def move_sound(self):
        sound=pygame.mixer.Sound("../assets/sounds/move.wav")
        pygame.mixer.Sound.play(sound)