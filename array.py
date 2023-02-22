
import json
import requests
import sys

import vpython
from vpython import vector as v

from models import ground
from models import tiles

SCENE = None
SUN = None
GROUND = None
TILE_LIST = None


def plot_tiles(obs=None, con=None):
    tile_list = []
    bad_tiles = obs['bad_tiles']
    g = ground.Ground()

    for tile_id_s in con.keys():
        tile_east = con[tile_id_s]['pos'][0]
        tile_north = con[tile_id_s]['pos'][1]
        tile_alt = con[tile_id_s]['altitude']
        receiver_id = con[tile_id_s]['receiver']
        slot = con[tile_id_s]['slot']
        tile_name = con[tile_id_s]['name']
        azimuth = obs['rfstreams']['0']['azimuth']
        elevation = obs['rfstreams']['0']['elevation']
        if tile_id_s in obs['rfstreams']['0']['bad_dipoles']:
            xbadlist, ybadlist = obs['rfstreams']['0']['bad_dipoles'][tile_id_s]
        else:
            xbadlist, ybadlist = [], []
        if tile_id_s in bad_tiles:
            tile_fault = True
        else:
            tile_fault = False

        print("Tile %s has bad dipoles: %s, %s" % (tile_id_s, xbadlist, ybadlist))

        delays = obs['alldelays'][tile_id_s]  # List of [xdelays, ydelays]
        t = tiles.Tile(cpos=v(tile_east, tile_north, 0.0),
                       tile_id=int(tile_id_s),
                       tile_name=tile_name,
                       xbadlist=xbadlist,
                       ybadlist=ybadlist,
                       receiver_id=receiver_id,
                       slot=slot,
                       azimuth=azimuth,
                       elevation=elevation,
                       delays=delays,
                       tile_fault=tile_fault)
        tile_list.append(t)
        print('Create tile %s' % tile_id_s)

    return g, tile_list

#
# def plot_receivers(obs=None, con=None):
#     for pad in pads:
#         pobj = vpython.box(pos=v(pad.east, pad.north, 0.0), length=1.0, height=2.0, width=1.0, color=color.white)
#         if not pad.enabled:
#             pobj.color = v(0.5, 0.5, 0.5)
#         num = int(''.join([c for c in pad.name if c.isdigit()]))
#         if divmod(num, 2)[1] == 0:
#             xoffset = 12
#         else:
#             xoffset = -12
#         if pad.name.endswith('a'):
#             yoffset = -8
#         else:
#             yoffset = 8
#         #    pobj.label = vpython.label(pos=pobj.pos, text=pad.name, xoffset=xoffset, yoffset=yoffset, box=False, line=False, opacity=0.2)
#         pobj.label = vpython.label(pos=v(pobj.pos.x + xoffset, pobj.pos.y + yoffset, pobj.pos.z + 10), text=pad.name,
#                                    height=15)
#         pobj.cables = {}
#         for tname, tdata in pad.inputs.items():
#             tpos = v(tdata[0].east, tdata[0].north, 0.0)
#             cobj = vpython.arrow(pos=pobj.pos, axis=(tpos - pobj.pos), shaftwidth=ARROWWIDTH, fixedwidth=True)
#             pobj.cables[tname] = cobj
#         pdict[pad.name] = pobj


def ProcessKeys(event):
    """Handle any keystrokes during the model.
    """
    try:  # Key pressed:
        k = event.key
        if (k == 'c'):  # Turn on complex view
            for t in TILE_LIST:
                t.complex()
        elif (k == 's'):   # Turn on simple view
            for t in TILE_LIST:
                t.simple()
        elif (k == 'r'):  # Re-center on 0,0,0
            SCENE.center = v(0, 0, 0)
    except:
        print('Exception in ProcessKeys')


def ProcessClicks(evt):
    loc = SCENE.mouse.project(normal=v(0,0,1))
    if loc:  # If we've clicked in a place in the X/Y plane
        SCENE.center = loc
    else:
        pass


def init(width, height):
    global SCENE, SUN
    SCENE = vpython.canvas(title='MWA Tile cabling', width=width, height=height, ambient=vpython.color.gray(0.8))
    SCENE.autocenter = False  # Disable auto-centering and point the camera at the origin to start
    SCENE.center = v(0, 0, 0)
    SCENE.lights = []
    # SUN = vpython.distant_light(direction=v(1500,  500,  10000), color=vpython.color.gray(0.8))
    SCENE.up = v(0, 1, 0)
    SCENE.show_rendertime = True
    SCENE.bind('keydown', ProcessKeys)
    SCENE.bind('click', ProcessClicks)


if __name__ == '__main__':
    init(1000, 1000)
    if len(sys.argv) > 1:
        obsid = int(sys.argv[1])
    else:
        obsid = None
    result = requests.get('http://ws.mwatelescope.org/metadata/obs', data={'obs_id': obsid})
    obs = json.loads(result.text)
    result = requests.get('http://ws.mwatelescope.org/metadata/con', data={'obs_id': obsid})
    con = json.loads(result.text)

    GROUND, TILE_LIST = plot_tiles(obs=obs, con=con)
    for t in TILE_LIST:
        t.simple()
    print('Turned on simple view')

    while True:
        vpython.rate(100)