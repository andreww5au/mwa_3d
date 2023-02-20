
import vpython
from vpython import color
from vpython import vector as v

from models import ground
from models import tiles

scene = None


def plot_tiles(obs=None, con=None):
    g = ground.Ground()
    tile_list = []

    for tile_id_s in con.keys():
        tile_east = con[tile_id_s]['pos'][0]
        tile_north = con[tile_id_s]['pos'][1]
        tile_alt = con[tile_id_s]['altitude']
        receiver_id = con[tile_id_s]['receiver']
        slot = con[tile_id_s]['slot']
        tile_name = con[tile_id_s]['name']
        azimuth = obs['rfstreams']['0']['azimuth']
        elevation = obs['rfstreams']['0']['elevation']
        xbadlist, ybadlist = obs['rfstreams']['0']['bad_dipoles'][tile_id_s]
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
                       delays=delays)
        tile_list.append(t)

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


def init(width, height):
    global scene
    scene = vpython.canvas(title='MWA Tile cabling', width=width, height=height)
    scene.autocenter = False  # Disable autocentering and point the camera at the origin to start
    scene.center = v(0, 0, 0)
    scene.show_rendertime = True

