# This code is part of KQCircuits
# Copyright (C) 2022 IQM Finland Oy
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see
# https://www.gnu.org/licenses/gpl-3.0.html.
#
# The software distribution should follow IQM trademark policy for open-source software
# (meetiqm.com/developers/osstmpolicy). IQM welcomes contributions to the code. Please see our contribution agreements
# for individuals (meetiqm.com/developers/clas/individual) and organizations (meetiqm.com/developers/clas/organization).

import sys
import logging

from kqcircuits.pya_resolver import pya
from kqcircuits.simulations.export.simulation_export import export_simulation_oas
from kqcircuits.simulations.export.ansys.ansys_export import export_ansys
from kqcircuits.simulations.waveguides_sim import WaveGuidesSim
from kqcircuits.util.export_helper import create_or_empty_tmp_directory, get_active_or_new_layout, \
    open_with_klayout_or_default_application

# This is a test case for initial mesh refinement (Ansys) via
# `gap_max_element_length` that restricts the element length in the gap.

sim_class = WaveGuidesSim  # pylint: disable=invalid-name
path = create_or_empty_tmp_directory("waveguide_eig_mesh_test")

box_size_x = 6000
box_size_y = 1000

sim_parameters = {
    'name': 'waveguides',
    'use_internal_ports': True,
    'use_edge_ports': False,
    'port_termination_end': False,
    'use_ports': True,
    'box': pya.DBox(pya.DPoint(-box_size_x/2., -box_size_y/2.), pya.DPoint(box_size_x/2., box_size_y/2.)),
    'cpw_length': 4000,  # if edge_ports then this has to be box_size_x
    'a': 10,
    'b': 6,
    'add_bumps': False,
    'wafer_stack_type': "planar",
    'n_guides': 1,
    'port_size': 50,
}

export_parameters_ansys = {
    'path': path,
    'ansys_tool': 'eigenmode',
    'maximum_passes': 2,
    'percent_refinement': 30,
    'gap_max_element_length': 4,
    'exit_after_run': True,
    'max_delta_f': 0.1,  # maximum relative difference for convergence in %
    'n_modes': 1,  # eigenmodes to solve
    'frequency': 10,  # minimum allowed eigenmode frequency
    'substrate_loss_tangent': 1e-6,  # Loss tangents for estimating quality factor
}

# Get layout
logging.basicConfig(level=logging.WARN, stream=sys.stdout)
layout = get_active_or_new_layout()

simulations = [sim_class(layout, **sim_parameters)]

# Create simulation
open_with_klayout_or_default_application(export_simulation_oas(simulations, path))

export_ansys(simulations, **export_parameters_ansys)
