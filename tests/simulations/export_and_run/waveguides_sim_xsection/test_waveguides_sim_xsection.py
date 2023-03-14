# This code is part of KQCircuits
# Copyright (C) 2023 IQM Finland Oy
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

from pathlib import Path
import sys
export_script_dir = Path(__file__).parent
sys.path.append(str(export_script_dir.parent))
from export_and_run_helper import assert_sim_script, export_and_run_test

generate_ref_results = False # set to True if you wish to update the
                             # reference results with what you get from your tests

def test_n_guides_1():
    _, export_path = export_and_run_test("waveguides_sim_xsection", ['--n-guides', '1'])

    project_ref_info = {
            'project_results_file': 'waveguides_n_guides_1_result.json',
            'ref_project_results_file': 'test_n_guides_1.json',
            'rtol': 1e-2,
            'atol': 1e-20,
            'ignore_keys': ['E_ground', 'E_signal_'],
        }

    assert_sim_script("waveguides_sim_xsection",
                      export_script_dir,
                      export_path,
                      project_ref_info,
                      generate_ref_results=generate_ref_results)

def test_london():
    _, export_path = export_and_run_test("waveguides_sim_xsection",
                                        ['--n-guides', '1', '--london-penetration-depth', '100e-9'])

    project_ref_info = {
            'project_results_file': 'waveguides_n_guides_1_result.json',
            'ref_project_results_file': 'test_london.json',
            'rtol': 1e-2,
            'atol': 1e-20,
            'ignore_keys': ['E_ground', 'E_signal_'],
        }

    assert_sim_script("waveguides_sim_xsection",
                      export_script_dir,
                      export_path,
                      project_ref_info,
                      generate_ref_results=generate_ref_results)
