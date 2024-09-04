from math import radians

import pygame
import constantes
import math
import random


class Weapon():
    def __init__(self, image, image_bullet):
        self.image_bullet = image_bullet
        self.image_original = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.shape = self.image.get_rect()
        self.shot = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = constantes.COOLDOWN_BULLETS
        bullet = None
        self.shape.center = player.shape.center
        if player.flip == False:
            self.shape.y = self.shape.y + player.shape.height / 6
            self.shape.x = self.shape.x + player.shape.width / 10
            self.rotate_weapon(False)
        if player.flip == True:
            self.shape.y = self.shape.y + player.shape.height / 6
            self.shape.x = self.shape.x - player.shape.width / 10
            self.rotate_weapon(True)

        #mover pistola con raton
        mouse_pos = pygame.mouse.get_pos()
        distance_x = mouse_pos[0] - self.shape.centerx
        distance_y = -(mouse_pos[1] - self.shape.centery)
        self.angle = math.degrees(math.atan2(distance_y, distance_x))

        #print(self.angle)

        #Detectar clicks
        if pygame.mouse.get_pressed()[0] and self.shot == False and (pygame.time.get_ticks()-self.last_shot >= shot_cooldown):
            bullet = Bullet(self.image_bullet, self.shape.centerx, self.shape.centery, self.angle)
            self.shot = True
            self.last_shot = pygame.time.get_ticks()
        #resetear click
        if pygame.mouse.get_pressed()[0] == False:
            self.shot = False
        return bullet

    def draw(self, interfaz):
        #self.image = pygame.transform.rotate(self.image,
                                             #self.angle)
        interfaz.blit(self.image, self.shape)
        #pygame.draw.rect(interfaz, constantes.COLOR_WEAPON, self.shape, 1)

    def rotate_weapon(self, rotate):
        if rotate == True:
            image_flip = pygame.transform.flip(self.image_original,
                                               True, False)
            self.image = pygame.transform.rotate(image_flip, self.angle)
        else:
            image_flip = pygame.transform.flip(self.image_original,
                                               False, False)
            self.image = pygame.transform.rotate(self.image_original, self.angle)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        #calcular velocidad
        self.delta_x = math.cos(radians(self.angle)) * constantes.BULLET_SPEED
        self.delta_y = math.sin(radians(self.angle)) * constantes.BULLET_SPEED

    def update(self, list_enemies):
        damage = 0
        pos_damage = None
        self.rect.x += self.delta_x
        self.rect.y = self.rect.y - self.delta_y

        #ver si balas se salen
        if self.rect.right < 0 or self.rect.left > constantes.WITHD_WINDOW or self.rect.bottom < 0 or self.rect.top > constantes.HEIGHT_WINDOW:
            self.kill()

        #verificar colisión:
        for enemy in list_enemies:
            if enemy.shape.colliderect(self.rect):
                damage = 15 + random.randint(-7, 7)
                pos_damage = enemy.shape
                enemy.energy -= damage
                #enemy.energy = enemy.energy - damage ES LO MISMO DE ARRIBA
                self.kill()
                break
        return damage, pos_damage

    def draw(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx + int(self.image.get_width()/2), self.rect.centery - int(self.image.get_height()/20)))

