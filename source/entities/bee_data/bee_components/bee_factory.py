"""
Class Name: Bee Factory
Class Purpose: Procedurally generates bee sprites
Notes:
"""

from os.path import join

from pygame import image, Surface, SRCALPHA


def make_head_dict():
    """
    Makes the dictionary of head files
    :return: dictionary of head sprites
    """
    h = {}
    for i in range(0, 12):
        h['head' + str(i)] = image.load(join('source', 'assets', 'sprites', 'bee_sprites', 'heads',
                                             'beeHead_' + str(i) + '.png'))
    return h


def make_torso_dict():
    """
    Makes the dictionary of torso files
    :return: dictionary of torso sprites
    """
    t = {}
    for i in range(0, 6):
        t['torso' + str(i)] = image.load(join('source', 'assets', 'sprites', 'bee_sprites', 'torsos',
                                              'torso_' + str(i) + '.png'))
    return t


def make_wings_dict():
    """
    Makes the dictionary of wing files
    :return: dictionary of wing sprites
    """
    w = {}
    for i in range(0, 6):
        w['wings_up' + str(i)] = image.load(join('source', 'assets', 'sprites', 'bee_sprites', 'wings', 'wings_u',
                                                 'wings_up' + str(i) + '.png'))
        w['wings_d' + str(i)] = image.load(join('source', 'assets', 'sprites', 'bee_sprites', 'wings', 'wings_d',
                                                'wings_down' + str(i) + '.png'))
    return w


heads = make_head_dict()
torsos = make_torso_dict()
wings = make_wings_dict()


def make_bee_sprites(genome):
    """
    Makes the bee sprites based on the provided genome
    :param genome: [(1-11), (1-5), (1-5)] Index 0 is the head gene, Index 2 is torso and Index 3,4 are the wings
    :return: wings up sprite, wings down sprite
    """
    head_gene = genome[0]
    head = heads['head' + str(head_gene)]

    wing_u_gene = genome[1]
    wings_u = wings['wings_up' + str(wing_u_gene)]
    wing_d_gene = genome[2]
    wings_d = wings['wings_d' + str(wing_d_gene)]

    torso_gene = genome[3]
    torso = torsos['torso' + str(torso_gene)]

    sprite_surf = Surface((18, 18), SRCALPHA)

    sprite_surf.blit(head, (6, 0))
    sprite_surf.blit(torso, (5, 11))

    wings_u_sprite = sprite_surf.copy()
    wings_d_sprite = sprite_surf.copy()

    wings_u_sprite.blit(wings_u, (0, 2))
    wings_d_sprite.blit(wings_d, (0, 6))

    return wings_u_sprite, wings_d_sprite
