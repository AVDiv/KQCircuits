# Copyright (c) 2019-2020 IQM Finland Oy.
#
# All rights reserved. Confidential and proprietary.
#
# Distribution or reproduction of any information contained herein is prohibited without IQM Finland Oy’s prior
# written permission.

import sys
import numpy
from importlib import reload

from kqcircuits.pya_resolver import pya

from kqcircuits.chips.chip import Chip

reload(sys.modules[Chip.__module__])

version = 1


class JunctionTest(Chip):
    """The PCell declaration for a JunctionTest chip."""

    PARAMETERS_SCHEMA = {
        "edge_len": {
            "type": pya.PCellParameterDeclaration.TypeInt,
            "description": "Length of square's one edge",
            "default": 80
        },
        "inter_space": {
            "type": pya.PCellParameterDeclaration.TypeInt,
            "description": "Space in between the Squares",
            "default": 20
        }
    }

    def produce_impl(self):

        # defining the parameters for local use
        edge_len = self.edge_len
        inter_space = self.inter_space

        left = self.box.left
        right = self.box.right
        top = self.box.top
        bottom = self.box.bottom

        width = right - left
        height = top - bottom

        # create the polygon
        poly = pya.DPolygon([
            pya.DPoint(left + 2000, bottom + 100 + self.dice_width),
            pya.DPoint(left + 2000, bottom + 2000),
            pya.DPoint(left + 100 + self.dice_width, bottom + 2000),
            pya.DPoint(left + 100 + self.dice_width, bottom + 8000),
            pya.DPoint(left + 2000, bottom + 8000),
            pya.DPoint(left + 2000, bottom + height - 100 - self.dice_width),
            pya.DPoint(left + 8000, bottom + height - 100 - self.dice_width),
            pya.DPoint(left + 8000, bottom + 8000),
            pya.DPoint(left + width - 100 - self.dice_width, bottom + 8000),
            pya.DPoint(left + width - 100 - self.dice_width, bottom + 2000),
            pya.DPoint(left + 8000, bottom + 2000),
            pya.DPoint(left + 8000, bottom + 100 + self.dice_width)
        ])

        # create the box array
        b_array = []

        for y in numpy.arange(bottom + self.dice_width + self.inter_space, bottom + height - self.dice_width,
                              self.edge_len + self.inter_space):
            for x in numpy.arange(left + self.dice_width + self.inter_space, left + width - self.dice_width,
                                  self.edge_len + self.inter_space):
                b = pya.DPolygon(pya.DBox(x, y, x + self.edge_len, y + self.edge_len)).to_itype(self.layout.dbu)
                b_array.append(b)

        # substract the box array from the polygon
        reg1 = pya.Region(poly.to_itype(self.layout.dbu))
        reg2 = pya.Region()

        for i in range(0, len(b_array)):
            reg2.insert(b_array[i])

        result = reg1 - reg2
        self.cell.shapes(self.get_layer("base metal gap wo grid")).insert(result)

        super().produce_impl()
