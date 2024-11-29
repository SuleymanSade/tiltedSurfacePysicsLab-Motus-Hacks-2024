# import pymunk
import pygame
import thorpy as tp

SCREEN_SIZE = (1200, 600)
pygame.init()

surface = pygame.Surface((10, 10))
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
tp.init(screen, tp.theme_human)

my_button = tp.Button("Hello, world.\nThis button uses the default theme.")
my_button.center_on(screen)
theta = tp.SliderWithText("Theta(θ)", 30, 60, 45, 200)
theta.set_bottomright(400,50)
mass = tp.SliderWithText("Mass", 30, 60, 45, 200)
mass.set_topleft(400,100)
slider4 = tp.SliderWithText("How many games should we play ?",
                                1, 10, 3, #min, max and initial values
                                50, "h", #length and orientation
                                dragger_size=(10,20),
                                show_value_on_right_side=True,
                                edit=True) #allow to edit value as a text
slider5 = tp.SliderWithText("Fine tune some number\n(from -2 to 2)", -2, 2, 1.5, 200,
                                round_decimals=3) #by default, 2 decimals
surfaceMaterialsDD = tp.DropDownListButton(
    choices= ["no friction", "ice", "rocky"],
    title="Surface Type",
)

group = tp.Group([theta, mass, slider5, my_button, surfaceMaterialsDD])
group.set_topleft(700,50)
def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((250,)*3)
    pygame.draw.rect(screen, (170, 170, 170), [100, 100, 40, 40])
    print(theta.get_value())

tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

#For the sake of brevity, the main loop is replaced here by a shorter but blackbox-like method
# player = my_button.get_updater().launch()

player = group.get_updater().launch(before_gui)

pygame.quit()

# space = pymunk.space()
# body = pymunk.body()
# rectangle = pymunk.Poly.create_box(body=body, size=(50, 50))
