from pygame import display, time, DOUBLEBUF

from settings_data import load_settings_file
from main_menu_loop import main_menu_loop
from settings_loop import settings_loop
from sim_loop import simulation_loop
from source.entities import sprite_bank

game_icon = sprite_bank.retrieve('game_icon')
game_clock = time.Clock()

game_states = {  # we don't actually use this, but it's convenient to have the dictionary written down somewhere
    0: 'main_menu',
    1: 'simulation',
    2: 'settings'
}


def init():
    state = 0
    display.init()
    settings = load_settings_file()
    screen = display.set_mode(settings.frame_resolution, DOUBLEBUF)
    display.set_caption("beeSim")
    display.set_icon(game_icon)

    return state, screen, settings


def main():
    state, screen, settings = init()

    while True:
        if state == 0:
            state = main_menu_loop(screen, game_clock, settings)
        elif state == 1:
            state = simulation_loop(screen, game_clock, settings)
        elif state == 2:
            state, screen, settings = settings_loop(screen, game_clock, settings)


if __name__ == "__main__":
    main()
