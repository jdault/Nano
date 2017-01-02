#INITIALIZATION
import pygame, math, sys
from pygame.locals import*
screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()

class GuySprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED=10
    MAX_REVERSE_SPEED=10
    ACCELERATION = 2
    TURN_SPEED = 5

    def __init__(self,image,position):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load('./assets/guyrun1.png'))
        self.images.append(pygame.image.load('./assets/guyrun2.png'))
        self.images.append(pygame.image.load('./assets/guyrun3.png'))
        self.images.append(pygame.image.load('./assets/guyrun2.png'))
        self.index = 0
        self.src_image = self.images[self.index]
        self.position = position
        self.speed = self.direction =self.height = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0

    def update(self,deltat):
        #SIMULATION
        self.speed += (self.k_right + self.k_left)
        self.height += self.k_up
        if self.height < 0:self.height+=1
        if self.k_right == 0 and self.k_left == 0 and self.speed != 0:self.speed += -(self.speed)/abs(self.speed)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        x += self.speed
        y += self.height
        if y <384 and self.height == 0 :y += 6
        self.position = (x,y)
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        if self.speed == 0: self.src_image = pygame.image.load('./assets/guystand.png')
        elif self.speed < 0: self.src_image = pygame.transform.flip(self.images[self.index],1,0)
        else: self.src_image = self.images[self.index]
        self.image = self.src_image
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        #print(str(self.k_up)+","+str(self.k_right)+","+str(self.k_left))

#CREATE A CAR AND RUN
rect = screen.get_rect()
guy = GuySprite('./assets/barrell.png',rect.center)
guy_group = pygame.sprite.RenderPlain(guy)
while 1:
    #USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT: guy.k_right = down*5
        elif event.key == K_LEFT: guy.k_left = down*-5
        elif event.key == K_UP: guy.k_up = down*-2
        elif event.key == K_DOWN: guy.k_down = down*2
        elif event.key == K_ESCAPE: sys.exit(0)
    #RENDERING
    screen.fill((255,255,255))
    guy_group.update(deltat)
    guy_group.draw(screen)
    pygame.display.flip()
