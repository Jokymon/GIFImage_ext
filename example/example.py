import pygame
import pygame.gfxdraw
from AnimatedGifSprite import *


class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, size=(100, 50), command=None):
        super().__init__()

        self.font = pygame.font.SysFont("Arial", 36)
        self.text = text
        self.command = command

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.rect.w, self.rect.h = size
        self.set_text(self.text)

    def set_text(self, text):
        pygame.draw.rect(self.image, "blue", self.image.get_rect())

        text_image = self.font.render(text, 1, "white")
        text_rect = text_image.get_rect(center=(self.rect.w/2, self.rect.h/2))
        self.image.blit(text_image, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.command is not None:
                    self.command()


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    dog = AnimatedGifSprite((50, 50), "example/dog_drinking_milk.gif")
    dog.scale(0.5)
    button_step = Button((500, 50), "Next",
        command = dog.next_frame)
    button_play = Button((500, 110), "Play",
        command = dog.play)
    button_pause = Button((500, 170), "Pause",
        command = dog.pause)

    sprite_group = pygame.sprite.Group()
    sprite_group.add(dog)
    sprite_group.add(button_step)
    sprite_group.add(button_play)
    sprite_group.add(button_pause)

    dog.pause()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            button_step.handle_event(event)
            button_play.handle_event(event)
            button_pause.handle_event(event)

        screen.fill((255,255,255))
        sprite_group.update(screen)
        sprite_group.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
