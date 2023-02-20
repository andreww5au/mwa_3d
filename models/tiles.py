__author__ = 'andrew'

import math

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

DELAYSTEP = 435.0  # Delay line increment in picoseconds
C = 0.000299798  # C in meters/picosecond


def getdipole(cpos=None, badx=None, bady=None):
    """
    Return the VPython elements making up a single dipole at position 'cpos'.

    Returns two sets of elements - a complext list, and a simple list, where all elements are initially not
    visible. The caller should loop over one of the element lists and set them to visible.

    :param cpos: absolute (x,y,z) coordinates of the dipole
    :param badx: True if the X dipole is bad (draw it in red)
    :param bady: True if the Y dipole is bad (draw it in red)
    :return: a tuple of (slist, clist) where clist contains the 'complex' elements (fiddly bits), and
             slist contains simple alternative versions of the dipole.
    """
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

    if badx is None:
        xcolor = vpython.color.gray(0.8)
    elif badx:
        xcolor = vpython.color.red
    else:
        xcolor = vpython.color.green

    if bady is None:
        ycolor = vpython.color.gray(0.8)
    elif bady:
        ycolor = vpython.color.red
    else:
        ycolor = vpython.color.green

    xpad = vpython.box(pos=v(0, 0, 0) + cpos,
                       axis=v(0, 0, 1),
                       height=width * 0.75,
                       width=width * 3,
                       length=standoff,
                       color=xcolor,
                       visible=False)

    ypad = vpython.box(pos=v(0, 0, 0.05) + cpos,
                       axis=v(0, 0, 1),
                       height=width * 3,
                       width=width * 0.75,
                       length=standoff,
                       color=ycolor,
                       visible=False)

    xl = vpython.box(pos=v(-width, 0, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw,
                     color=xcolor,
                     visible=False)
    xlt = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(width, 0, standoff) - v(-width, 0, height)),
                      height=boxw,
                      width=boxw,
                      color=xcolor,
                      visible=False)
    xlb = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(width, 0, height) - v(-width, 0, standoff)),
                      height=boxw,
                      width=boxw,
                      color=xcolor,
                      visible=False)
    xr = vpython.box(pos=v(width, 0, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw,
                     color=xcolor,
                     visible=False)

    yl = vpython.box(pos=v(0, -width, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw,
                     color=ycolor,
                     visible=False)
    ylt = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(0, width, standoff) - v(0, -width, height)),
                      height=boxw,
                      width=boxw,
                      color=ycolor,
                      visible=False)
    ylb = vpython.box(pos=v(0, 0, cpoint.z) + cpos,
                      axis=(v(0, width, height) - v(0, -width, standoff)),
                      height=boxw,
                      width=boxw,
                      color=ycolor,
                      visible=False)
    yr = vpython.box(pos=v(0, width, (height + standoff) / 2) + cpos,
                     axis=v(0, 0, 1),
                     height=boxw,
                     width=boxw,
                     length=height + boxw,
                     color=ycolor,
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
    return [xpad, ypad], [xl, xlt, xlb, xr, yl, ylt, ylb, yr, lna, tube]


class Tile():
    """
    Represents a single MWA tile, ground mesh, and beamformer.
    """

    def __init__(self,
                 tile_id=0,
                 tile_name='',
                 cpos=None,
                 xbadlist=None,
                 ybadlist=None,
                 receiver_id=None,
                 slot=None,
                 azimuth=None,
                 elevation=None,
                 delays=None):
        if cpos is None:
            cpos = v(0, 0, 0)
        elif type(cpos) == tuple:
            cpos = v(cpos)

        self.cpos = cpos
        self.tile_id = tile_id
        self.tile_name = tile_name
        self.receiver_id = receiver_id
        self.slot = slot
        self.azimuth = azimuth
        self.elevation = elevation

        if xbadlist is None:
            xbadlist = []

        if ybadlist is None:
            ybadlist = []

        if delays is None:
            self.xdelays = []
            self.ydelays = []
        else:
            self.xdelays = delays[0]
            self.ydelays = delays[1]

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

        self.slist = []
        self.clist = []
        for i in range(16):
            simp, comp = getdipole(cpos=v(xoffsets[i], yoffsets[i], 0) + cpos,
                                   badx=((i + 1) in xbadlist),
                                   bady=((i + 1) in ybadlist))
            if self.xdelays and (self.xdelays[i] != 32)  and (self.xdelays[i] != 0) and (self.azimuth is not None) and (self.elevation is not None):
                d = v(0, 1, 0)   # North
                d.rotate(self.elevation * math.pi / 180.0, (-1, 0, 0))  # Rotate 'elevation' degrees around a vector due East
                d.rotate(self.azimuth * math.pi / 180.0, (0, 0, 1))   # Rotate 'azimuth' degrees around the zenith vector
                da = vpython.arrow(cpos=v(xoffsets[i], yoffsets[i], 0) + cpos,
                                   axis=d,
                                   length=self.xdelays[i] * DELAYSTEP * C,  # Dipole delay in metres, at 'c'
                                   shaftwidth=0.4,
                                   fixedwidth=True,
                                   visible=False)
                self.clist.append(da)
            self.slist += simp
            self.clist += comp

    def complex(self):
        for d in self.clist:
            d.visible = True
        for d in self.slist:
            d.visible = False
        self.gp.visible = True
        self.bf.visible = True

    def simple(self):
        for d in self.clist:
            d.visible = False
        for d in self.slist:
            d.visible = True
        self.gp.visible = True
        self.bf.visible = False

    def none(self):
        for d in self.clist:
            d.visible = False
        for d in self.slist:
            d.visible = False
        self.gp.visible = False
        self.bf.visible = False

