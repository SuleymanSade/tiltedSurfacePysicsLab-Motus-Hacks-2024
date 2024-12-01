import math
import pygame
import thorpy as tp

# Constants
SCREEN_SIZE = (1200, 600)
LINE_CENTER_COORD = (100,500)
LINE_CENTER_X = LINE_CENTER_COORD[0]
LINE_CENTER_Y = LINE_CENTER_COORD[1]
LINE_X_L = 500
SQUARE_SIDE_L = 50



pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

tp.init(screen, tp.theme_human)

runButton = tp.Button(">")
runButton.center_on(screen)
theta = tp.SliderWithText("Theta(θ)", 15, 45, 30, 200)
theta.set_bottomright(400,50)
mass = tp.SliderWithText("Mass(kg)", 10, 20, 15, 200)
mass.set_topleft(400,100)

view_time = tp.Text("Time(s):")


# surfaceMaterialsDD = tp.DropDownListButton(
#     choices= ["no friction", "ice", "rocky"],
#     title="Surface Type",
#     generate_shadow= (False, 'auto')
# )


group = tp.Group([theta, mass, runButton, view_time])
group.set_topleft(700,50)

rect_surface = pygame.Surface((SQUARE_SIDE_L,)*2, pygame.SRCALPHA)
rect_surface.fill((120,)*3)

rectX = 0
rectY = 0

ending_point_X =0
ending_point_Y =0

sim_time=0

final_time=0

def update_pos():
    global ending_point_X, ending_point_Y, rectX, rectY

    hypotenuse = LINE_X_L #*math.cos(theta.get_value()*(math.pi/180))
    ending_point_Y = LINE_CENTER_Y - (hypotenuse*math.sin(theta.get_value()*(math.pi/180)))
    ending_point_X = LINE_CENTER_X + (hypotenuse*math.cos(theta.get_value()*(math.pi/180)))
    
    rectX = ending_point_X
    rectY = ending_point_Y
                       

def start_sim():
    global sim_started_bool, sim_time
    accel = (mass.get_value()*9.81) * math.sin(theta.get_value()*(math.pi/180))
    sim_time =0
    print(accel)
    sim_started_bool = True
    
sim_started_bool = False

runButton.at_unclick = start_sim

def before_gui(): # Main loop, this approach is used because of thorPy library
    global ending_point_X, ending_point_Y, rectX, rectY, sim_time, sim_started_bool
    
    update_pos()
    
    if sim_started_bool:
        sim_time+=1

        accel = (mass.get_value()*9.81) * math.sin(theta.get_value()*(math.pi/180))
        accel_X = accel * math.cos(theta.get_value()*(math.pi/180))
        accel_Y = accel * math.sin(theta.get_value()*(math.pi/180))
        
        change_x = accel_X * math.pow(sim_time/60, 2)
        change_y = accel_Y * math.pow(sim_time/60, 2)
        
        rectX-=change_x
        rectY+=change_y
        
        view_time.set_text(f'Time: {round(sim_time/60, 3)}')
        
    if(rectX<=100):
        sim_started_bool = False
        
        
    screen.fill((250,)*3)
    
    rect_surface_rot = pygame.transform.rotate(rect_surface, theta.get_value())
    rect_center = rect_surface_rot.get_rect(center=(rectX - SQUARE_SIDE_L // 2, rectY - SQUARE_SIDE_L // 2 +(5*(theta.get_value()/15))))  # +(5*(theta.get_value()/15))
    
    screen.blit(rect_surface_rot, rect_center)

    pygame.draw.line(screen, (10,130,10), (0, LINE_CENTER_Y), (LINE_CENTER_X+ LINE_X_L, LINE_CENTER_Y), 10)
    pygame.draw.line(screen, (0,0,0), LINE_CENTER_COORD, (ending_point_X, ending_point_Y), 10)
    pygame.draw.circle(screen, (165,42,42), LINE_CENTER_COORD, 10)
    
    clock.tick(60)
    
tp.call_before_gui(before_gui) # tells thorpy to call before_gui() before drawing gui.

player = group.get_updater().launch(before_gui)

pygame.quit()