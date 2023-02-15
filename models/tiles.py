__author__ = 'andrew'

import vpython
from vpython import color
from vpython import vector as v

pdict = {}

simplist = []
complist = []

ARROWWIDTH = 1.0

seltile = None
tlabel = None
scene = None


def getdipole(cpos=None):
    width = 0.35  # Center to edge of bat-wing
    height = 0.4  # Top of bat-wing corner to ground
    standoff = 0.1  # ground to bottom of bat-wing triangle
    cylen = 0.15  # length of LNA cylinder
    cydia = 0.15  # diameter of LNA cylinder
    cpoint = v(0, 0, (height / 2.0 + standoff))
    boxw = 0.05  # thickness of dipole arms
    tubeoff = standoff  # gap between bottom of wire tube and the ground
    if cpos is None:
        cpos = v((0, 0, 0))
    elif type(cpos) == tuple:
        cpos = v(cpos)

    xl = vpython.box(pos=v(-width, 0, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw,
                     color=vpython.color.gray(0.8),
                     visible=False)
    xlt = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(width, 0, standoff) - v(-width, 0, height)),
                      height=boxw,
                      width=boxw,
                      color=vpython.color.gray(0.8),
                      visible=False)
    xlb = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(width, 0, height) - v(-width, 0, standoff)),
                      height=boxw,
                      width=boxw,
                      color=vpython.color.gray(0.8),
                      visible=False)
    xr = vpython.box(pos=v(width, 0, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw,
                     color=vpython.color.gray(0.8),
                     visible=False)

    yl = vpython.box(pos=v(0, -width, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw,
                     color=vpython.color.gray(0.8),
                     visible=False)
    ylt = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(0, width, standoff) - v(0, -width, height)),
                      height=boxw,
                      width=boxw,
                      color=vpython.color.gray(0.8),
                      visible=False)
    ylb = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(0, width, height) - v(0, -width, standoff)),
                      height=boxw,
                      width=boxw,
                      color=vpython.color.gray(0.8),
                      visible=False)
    yr = vpython.box(pos=v(0, width, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw, color=vpython.color.gray(0.8),
                     visible=False)

    lna = vpython.cylinder(pos=v(0, 0, cpoint.z - cylen / 2) + cpos,
                           axis=v(0, 0, cylen),
                           radius=cydia / 2.0,
                           color=color.white,
                           visible=False)
    tube = vpython.cylinder(pos=v(0,0,tubeoff) + cpos,
                            radius=boxw/2.0,
                            axis=v(0,0,cpoint.z-standoff),
                            color=color.white,
                            visible=False)
    return [xl, xlt, xlb, xr, yl, ylt, ylb, yr, lna, tube]


class Tile():
    """
    Represents a single MWA tile, ground mesh, and beamformer.
    """

    def __init__(self, cpos=None):
        if cpos is None:
            cpos = v(0, 0, 0)
        elif type(cpos) == tuple:
            cpos = v(cpos)

        dip_sep = 1.10  # dipole separations in meters
        xoffsets = [0.0] * 16  # offsets of the dipoles in the W-E 'x' direction
        yoffsets = [0.0] * 16  # offsets of the dipoles in the S-N 'y' direction
        xoffsets[0] = -1.5 * dip_sep
        xoffsets[1] = -0.5 * dip_sep
        xoffsets[2] = 0.5 * dip_sep
        xoffsets[3] = 1.5 * dip_sep
        xoffsets[4] = -1.5 * dip_sep
        xoffsets[5] = -0.5 * dip_sep
        xoffsets[6] = 0.5 * dip_sep
        xoffsets[7] = 1.5 * dip_sep
        xoffsets[8] = -1.5 * dip_sep
        xoffsets[9] = -0.5 * dip_sep
        xoffsets[10] = 0.5 * dip_sep
        xoffsets[11] = 1.5 * dip_sep
        xoffsets[12] = -1.5 * dip_sep
        xoffsets[13] = -0.5 * dip_sep
        xoffsets[14] = 0.5 * dip_sep
        xoffsets[15] = 1.5 * dip_sep

        yoffsets[0] = 1.5 * dip_sep
        yoffsets[1] = 1.5 * dip_sep
        yoffsets[2] = 1.5 * dip_sep
        yoffsets[3] = 1.5 * dip_sep
        yoffsets[4] = 0.5 * dip_sep
        yoffsets[5] = 0.5 * dip_sep
        yoffsets[6] = 0.5 * dip_sep
        yoffsets[7] = 0.5 * dip_sep
        yoffsets[8] = -0.5 * dip_sep
        yoffsets[9] = -0.5 * dip_sep
        yoffsets[10] = -0.5 * dip_sep
        yoffsets[11] = -0.5 * dip_sep
        yoffsets[12] = -1.5 * dip_sep
        yoffsets[13] = -1.5 * dip_sep
        yoffsets[14] = -1.5 * dip_sep
        yoffsets[15] = -1.5 * dip_sep

        self.gp = vpython.box(pos=v(0, 0, 0) + cpos,
                              axis=v(0, 0, 1),
                              height=5.0,
                              width=5.0,
                              length=0.05,
                              color=color.gray(0.5),
                              visible=False)

        self.bf = vpython.box(pos=v(0, -3.5, 0.15) + cpos,
                              axis=v(0, 0, 1),
                              height=0.3,
                              width=0.4,
                              length=0.2,
                              color=color.white,
                              visible=False)
        self.dlist = []
        for i in range(16):
            self.dlist += getdipole(cpos=v(xoffsets[i], yoffsets[i], 0) + cpos)

    def complex(self):
        for d in self.dlist:
            d.visible = True
        self.gp.visible = True
        self.bf.visible = True

    def simple(self):
        for d in self.dlist:
            d.visible = False
        self.gp.visible = True
        self.bf.visible = False

    def none(self):
        for d in self.dlist:
            d.visible = False
        self.gp.visible = False
        self.bf.visible = False


def plot(tiles=None, pads=None):
    global simplist, complist, pdict, scene
    scene.autocenter = False  # Disable autocentering and point the camera at the origin to start
    scene.center = v(0, 0, 0)
    scene.show_rendertime = True

    # Draw a transparent grey ground plane, and transparent blue axis arrows and labels
    ground = vpython.box(pos=v(0, 0, 0), length=3000, height=3000, width=0.1, color=v(0.8, 0, 0), opacity=0.2)

    eaxis = vpython.arrow(pos=v(0, 0, 0), axis=v(1600, 0, 0), color=color.blue, shaftwidth=2, fixedwidth=True,
                          opacity=0.2)
    eaxislabel = vpython.label(text='East', pos=v(1580, 20, 0), color=color.blue)

    naxis = vpython.arrow(pos=v(0, 0, 0), axis=v(0, 1600, 0), color=color.blue, shaftwidth=2, fixedwidth=True,
                          opacity=0.2)
    naxislabel = vpython.label(text='North', pos=v(20, 1580, 0), color=color.blue)

    #  aaxis = vpython.arrow(pos=(0,0,0), axis=(0,0,100), color=color.blue, shaftwidth=2, fixedwidth=True, opacity=0.2)
    #  aaxislabel = vpython.label(text='Up', pos=(0,20,80), color=color.blue)

    for tile in tiles:
        #    complist += gettile(cpos=v(tile.east, tile.north, 0.0))
        simplist.append(vpython.box(pos=v(tile.east, tile.north, 0.0),
                                    axis=v(0, 0, 1),
                                    height=5.0,
                                    width=5.0,
                                    length=0.2,
                                    color=color.green))
        simplist[-1].name = tile.name

    for pad in pads:
        pobj = vpython.box(pos=v(pad.east, pad.north, 0.0), length=1.0, height=2.0, width=1.0, color=color.white)
        if not pad.enabled:
            pobj.color = v(0.5, 0.5, 0.5)
        num = int(''.join([c for c in pad.name if c.isdigit()]))
        if divmod(num, 2)[1] == 0:
            xoffset = 12
        else:
            xoffset = -12
        if pad.name.endswith('a'):
            yoffset = -8
        else:
            yoffset = 8
        #    pobj.label = vpython.label(pos=pobj.pos, text=pad.name, xoffset=xoffset, yoffset=yoffset, box=False, line=False, opacity=0.2)
        pobj.label = vpython.label(pos=v(pobj.pos.x + xoffset, pobj.pos.y + yoffset, pobj.pos.z + 10), text=pad.name,
                                   height=15)
        pobj.cables = {}
        for tname, tdata in pad.inputs.items():
            tpos = v(tdata[0].east, tdata[0].north, 0.0)
            cobj = vpython.arrow(pos=pobj.pos, axis=(tpos - pobj.pos), shaftwidth=ARROWWIDTH, fixedwidth=True)
            pobj.cables[tname] = cobj
        pdict[pad.name] = pobj

    # Bind mouse click events and key presses to the callback function
    scene.bind('mousedown', processClick)


def update(pad=None, tname=None, fixed=False, color=None):
    pobj = pdict[pad.name]
    if fixed:
        ccolor = vpython.color.orange
    else:
        ccolor = vpython.color.white
    if (color is not None):
        ccolor = color
        if (color != v(1.0, 1.0, 1.0)):
            #      wmult = 3   # only useful for plots showing lightning
            wmult = 1
        else:
            wmult = 1
    else:
        wmult = 1
    if (tname is not None) and (tname in pad.inputs):
        tpos = v(pad.inputs[tname][0].east, pad.inputs[tname][0].north, 0.0)
        cobj = vpython.arrow(pos=pobj.pos, axis=(tpos - pobj.pos), shaftwidth=ARROWWIDTH * wmult, fixedwidth=True,
                             color=ccolor)
        pobj.cables[tname] = cobj
    else:
        for cable in pobj.cables.values():
            cable.visible = False
        pobj.cables = {}
        for tname, tdata in pad.inputs.items():
            tpos = v(tdata[0].east, tdata[0].north, 0.0)
            cobj = vpython.arrow(pos=pobj.pos, axis=(tpos - pobj.pos), shaftwidth=ARROWWIDTH * wmult, fixedwidth=True,
                                 color=ccolor)
            pobj.cables[tname] = cobj


def trunk(pad=None):
    pobj = pdict[pad.name]
    trcolor = v(0.0, 0.9, 0.9)
    trobj = vpython.arrow(pos=v(0, 0, 0), axis=pobj.pos, shaftwidth=ARROWWIDTH * 3, fixedwidth=True, color=trcolor)
    trobj.visible = True


def processClick(event):
    global seltile, tlabel, scene
    try:  # Key pressed:
        s = event.key
        if s == 'c':
            for ob in simplist:
                ob.visible = False
            for ob in complist:
                ob.visible = True
        elif s == 's':
            for ob in complist:
                ob.visible = False
            for ob in simplist:
                ob.visible = True
    except AttributeError:  # Mouse clicked:
        clickedpos = scene.mouse.project(normal=v(0, 0, 1), d=0)  # Mouse position projected onto XY plane
        if clickedpos:
            scene.center = clickedpos  # Change the camera centre position
        ob = scene.mouse.pick
        try:
            name = ob.name
            if seltile is not None:
                seltile.color = color.green
                tlabel.visible = False
                del tlabel
            seltile = ob
            seltile.color = color.red
            tlabel = vpython.label(pos=v(seltile.pos.x, seltile.pos.y, seltile.pos.z + 10), text=name, height=15)
        except AttributeError:
            pass


def init(width, height):
    global scene
    scene = vpython.canvas(title='MWA Tile cabling', width=width, height=height)
