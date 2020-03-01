"""
File Name: Menus
File Purpose: Holds a variety of data needed for rendering menus and other UI elements
Notes:
"""

#  IMPORTS
from pygame import font, Surface
from source.entities import sprite_bank

# DATA FIELDS
menu_image = sprite_bank.retrieve('menu_image')
inspection_menu = sprite_bank.retrieve('inspection_menu')
highlight_button = sprite_bank.retrieve('inspection_button')

font.init()
gameFont = font.Font("source/assets/fonts/m5x7.ttf", 30)

# These are the locations of where different things are going to be rendered
fps_location = (20, 800)
bee_number_location = (20, 820)
inspection_menu_location = (50, 300)
bee_highlight_location = (20, 240)

# FUNCTIONS


def menu_render(entity_master, game_clock, inspection_target):
    menu_surface = Surface((400, 900))
    menu_surface.blit(menu_image, (0, 0))

    if inspection_target is not None:
        inspection_menu_surface = Surface((300, 300))
        inspection_menu_surface.blit(inspection_menu, (0, 0))

        bees_total = inspection_target.get_bees()
        bees_total_text = gameFont.render("Hive Population: "+str(bees_total[0]+bees_total[1]), False, [0, 0, 0], None)
        inspection_menu_surface.blit(bees_total_text, (10, 10))

        worker_text = gameFont.render("Workers: "+str(bees_total[0]), False, [0, 0, 0], None)
        inspection_menu_surface.blit(worker_text, (10, 30))

        scout_text = gameFont.render("Scouts: "+str(bees_total[1]), False, [0, 0, 0], None)
        inspection_menu_surface.blit(scout_text, (10, 50))

        hive_nectar = inspection_target.get_nectar()
        nectar_text = gameFont.render("Nectar Storage: "+str(hive_nectar), False, [0, 0, 0], None)
        inspection_menu_surface.blit(nectar_text, (10, 70))

        highlight_button_text = gameFont.render("Inspect Hive", False, [0, 0, 0], None)
        inspection_menu_surface.blit(highlight_button, bee_highlight_location)
        inspection_menu_surface.blit(highlight_button_text,
                                     (bee_highlight_location[0]+50, bee_highlight_location[1]+7))

        menu_surface.blit(inspection_menu_surface, inspection_menu_location)

    menu_surface.blit(update_fps_display(game_clock), fps_location)
    menu_surface.blit(number_of_bees(entity_master), bee_number_location)

    return menu_surface


def number_of_bees(entity_master):
    bee_num = entity_master.get_bee_population()
    render = gameFont.render("Bee Population: "+str(bee_num), False, [0, 0, 0], None)
    return render


def update_fps_display(game_clock):
    fps = game_clock.get_fps()
    fps_display = gameFont.render("FPS: "+str(fps)[0:4], False, [0, 0, 0], None)
    return fps_display
