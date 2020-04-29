from pygame import display, time

from main_menu_loop import main_menu_loop
from sim_loop import simulation_loop
from source.entities import sprite_bank

frame_resolution = [1600, 900]
game_icon = sprite_bank.retrieve('game_icon')
game_clock = time.Clock()
game_frame_rate = 90

game_states = {  # we don't actually use this, but it's convenient to have the dictionary written down somewhere
    0: 'main_menu',
    1: 'simulation'
}


def init():
    state = 0
    screen = display.set_mode(frame_resolution)
    display.set_caption("beeSim")
    display.set_icon(game_icon)
    return state, screen


def main():
    state, screen = init()

    while True:
        if state == 0:
            state = main_menu_loop(screen, frame_resolution, game_clock, game_frame_rate)
        elif state == 1:
            state = simulation_loop(screen, frame_resolution, game_clock, game_frame_rate)


if __name__ == "__main__":
    main()
