import pygame
from docutils.nodes import image

import constantes

class Personaje():
    def __init__(self, x, y, animations, energy):
        self.energy = energy
        self.alive = True
        self.flip = False
        self.animations = animations
        #imagen animación que se muestra actualmente
        self.frame_index = 0
        #aquí se almacena la hora actual en milisegundos desde que se inició
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = self.image.get_rect()

        #self.shape = pygame.Rect(0, 0, constantes.HEIHGT_PERSONAJE,
                                 #constantes.WITDH_PERSONAJE )
        self.shape.center = (x,y)

    def move(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y

    def update(self):
        #comprobar si está vivo
        if self.energy <= 0:
            self.energy = 0
            self.alive = False

        cooldown_animation = 70
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0




    def draw(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.shape)
        #pygame.draw.rect(interfaz, constantes.COLOR_PERSONAJE, self.shape, 1)
