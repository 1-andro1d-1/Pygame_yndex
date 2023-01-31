from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from interaction import Interaction
from moviepy.editor import *
import time


def play():
    while True:

        player.movement()
        drawing.background(player.angle)
        walls, wall_shot = ray_casting_walls(player, drawing.textures)
        drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
        drawing.fps(clock)
        drawing.mini_map(player)
        drawing.player_weapon([wall_shot, sprites.sprite_shot])

        interaction.interaction_objects()
        interaction.npc_action()
        interaction.clear_world()
        if LOOSE:
            break
        s = interaction.check_win()
        if s:
            time.sleep(3)
            break
        pygame.display.flip()
        clock.tick()


clip = VideoFileClip(r"start_video.mp4")
clip.preview()


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
loud_anim = [pygame.image.load(f'louding/louding {i}.png').convert_alpha() for i in range(14)]
now_img = 0
while now_img < 13:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        sc.blit(loud_anim[now_img], (0, 0))
        if pygame.mouse.get_pressed()[0]:
            now_img += 1
        if now_img > 10:
            break
    pygame.display.flip()


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock)
interaction = Interaction(player, sprites, drawing)
interaction.play_music()

drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()




play()

sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map, player, clock)
drawing.menu()


