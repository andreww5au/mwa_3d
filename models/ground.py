
import vpython
from vpython import color
from vpython import textures
from vpython import vector as v


class Ground():
    def __init__(self):
        # Draw a transparent grey ground plane, and transparent blue axis arrows and labels
        ground = vpython.box(pos=v(0, 0, -0.01),
                             length=3000,
                             height=3000,
                             width=0.01,
                             color=v(1.0, 0.6, 0.3),
                             opacity=0.8,
                             texture=textures.stucco)

        eaxis = vpython.arrow(pos=v(0, 0, 0), axis=v(1600, 0, 0), color=color.white, shaftwidth=3, fixedwidth=True,
                              opacity=0.8)
        eaxislabel = vpython.label(text='East', pos=v(1580, 20, 0), color=color.white)

        naxis = vpython.arrow(pos=v(0, 0, 0), axis=v(0, 1600, 0), color=color.white, shaftwidth=3, fixedwidth=True,
                              opacity=0.8)
        naxislabel = vpython.label(text='North', pos=v(20, 1580, 0), color=color.white)

        self.slist = [ground, eaxis, eaxislabel, naxis, naxislabel]
        self.clist = []

    def complex(self):
        for d in self.clist:
            d.visible = True
        for d in self.slist:
            d.visible = False

    def simple(self):
        for d in self.clist:
            d.visible = False
        for d in self.slist:
            d.visible = True

    def none(self):
        for d in self.clist:
            d.visible = False
        for d in self.slist:
            d.visible = False
