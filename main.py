import pygame
import constantes
from player import Personaje
from weapons import Weapon
import os
from texts import DamageText

#funciones:
#función escalar imagen:
def  scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    new_image = pygame.transform.scale(image, (w*scale, h*scale))
    return new_image

#función contar elementos:
def count_elements(directory):
    return len(os.listdir(directory))

#función listar nombre elementos:
def names_folders(directory):
    return os.listdir(directory)



pygame.init()
window = pygame.display.set_mode((constantes.WITHD_WINDOW,
                                  constantes.HEIGHT_WINDOW))
pygame.display.set_caption("Mi primer juego")

#fuentes
font = pygame.font.Font("assets//fonts//DungeonFont.ttf", 25)

#importar imágenes
#energia:
empty_heart = pygame.image.load("assets/images/items/empty_heart.png")
empty_heart = scale_img(empty_heart, constantes.SCALE_HEART)
half_heart = pygame.image.load("assets/images/items/half_heart.png")
half_heart = scale_img(half_heart, constantes.SCALE_HEART)
full_heart = pygame.image.load("assets/images/items/full_heart2.png")
full_heart = scale_img(full_heart, constantes.SCALE_HEART)

#player
animations = []
for i in range (8):
    img = pygame.image.load(f"assets//images//characters//player//walk_{i}.png")
    img = scale_img(img, constantes.SCALE_PLAYER)
    animations.append(img)

#enemies
directory_enemies = "assets//images//characters//enemies"
type_enemies = names_folders(directory_enemies)
animations_enemies = []
for eni in type_enemies:
    list_temp = []
    rute_temp = f"assets//images//characters//enemies//{eni}"
    num_animations = count_elements(rute_temp)
    for i in range(num_animations):
        img_enemy = pygame.image.load(f"{rute_temp}//{eni}_{i + 1}.png").convert_alpha()
        img_enemy = scale_img(img_enemy, constantes.SCALE_ENEMY)
        list_temp.append(img_enemy)
    animations_enemies.append(list_temp)


#Arma
image_shotgun = pygame.image.load(f"assets//images//weapons//weaponR3.png")
image_shotgun = scale_img(image_shotgun, constantes.SCALE_WEAPON)

#Balas
image_bullet = pygame.image.load(f"assets//images//weapons//bullet.png")
image_bullet = scale_img(image_bullet, constantes.SCALE_BULLET)

#vidas

def player_life():
    for i in range(4):
        if player.energy >= ((i+1)*25):
            window.blit(full_heart, (5+i*50, 5))
        elif player.energy % 25 > 0:
            window.blit(half_heart, (5+i*50, 5))


#crear jugador personaje
player = Personaje(50, 50, animations, 100)

#crear enemigo Personaje:
rosa = Personaje(400, 300, animations_enemies[0], 100)
amarillo = Personaje(200, 200, animations_enemies[1], 100)
rojo = Personaje(100, 250, animations_enemies[2], 100)

#crear lista enemigos:
list_enemies = []
list_enemies.append(rosa)
list_enemies.append(amarillo)
list_enemies.append(rojo)


#crear arma jugador:
shotgun = Weapon(image_shotgun, image_bullet)

#crear un grupo de sprites:
group_damage_text = pygame.sprite.Group()
group_bullet = pygame.sprite.Group()

#dibujar corazones
player_life()

#definir variables movimiento:
move_up = False
move_down = False
move_left = False
move_right = False

#controlar frame rate
clock = pygame.time.Clock()

run = True
while run == True:

    #60 FPS please
    clock.tick(constantes.FPS)

    window.fill(constantes.COLOR_BG)

    #Calcular movimiento jugador
    delta_x = 0
    delta_y = 0

    if move_right == True:
        delta_x = constantes.SPEED
    if move_left == True:
        delta_x = -constantes.SPEED
    if move_up == True:
        delta_y = -constantes.SPEED
    if move_down == True:
        delta_y = constantes.SPEED

    #Mover jugador
    player.move(delta_x, delta_y)

    #actualiza jugador
    player.update()

    #actualiza enemigos
    for ene in list_enemies:
        ene.update()
        print(ene.energy)

    #actualiza balas

    bullet = shotgun.update(player)
    if bullet:
        group_bullet.add(bullet)
    for bullet in group_bullet:
        damage, pos_damage = bullet.update(list_enemies)
        if damage:
            damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.ROJO)
            group_damage_text.add(damage_text)


    #actualizar daño:
    group_damage_text.update()

    #dibujar
    player.draw(window)
    shotgun.draw(window)
    for ene in list_enemies:
        ene.draw(window)

    for bullet in group_bullet:
        bullet.draw(window)

    #Dibujar textos:
    group_damage_text.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_s:
                move_down = False


    pygame.display.update()

pygame.quit()

