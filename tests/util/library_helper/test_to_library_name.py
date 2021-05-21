# This code is part of KQCircuits
# Copyright (C) 2021 IQM Finland Oy
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


import logging

import pytest

from kqcircuits.util.library_helper import to_library_name

log = logging.getLogger(__name__)


# SINGLE WORD TESTS

# normal cases

def test_pascal_case():
    result = to_library_name("AbcXyz")
    assert result == "Abc Xyz"


def test_pascal_case_with_single_uppercase_letter():
    result = to_library_name("ABcXyz")
    assert result == "ABc Xyz"


def test_pascal_case_with_multiple_single_uppercase_letters():
    result = to_library_name("ABcXYz")
    assert result == "ABc XYz"


# edge cases

def test_camel_case():
    with pytest.raises(ValueError) as info:
        to_library_name("abcXyz")
    assert str(info.value) == "PEP8 compliant class name 'abcXyz' must be PascalCase without underscores."


def test_snake_case():
    with pytest.raises(ValueError) as info:
        to_library_name("abc_xyz")
    assert str(info.value) == "PEP8 compliant class name 'abc_xyz' must be PascalCase without underscores."


def test_kebab_case():
    with pytest.raises(ValueError) as info:
        to_library_name("abc-xyz")
    assert str(info.value) == "Cannot convert invalid Python class name 'abc-xyz' to library name."


def test_space():
    with pytest.raises(ValueError) as info:
        to_library_name("abc xyz")
    assert str(info.value) == "Cannot convert invalid Python class name 'abc xyz' to library name."


def test_mixed_case_word():
    result = to_library_name("ABcXyZ")
    assert result == "ABc Xy Z"


def test_without_input():
    with pytest.raises(ValueError) as info:
        to_library_name()
    assert str(info.value) == "Cannot convert nil or non-string class name 'None' to library name."


def test_none():
    with pytest.raises(ValueError) as info:
        to_library_name(None)
    assert str(info.value) == "Cannot convert nil or non-string class name 'None' to library name."


def test_empty_string():
    with pytest.raises(ValueError) as info:
        to_library_name("")
    assert str(info.value) == "Cannot convert nil or non-string class name '' to library name."


def test_number():
    with pytest.raises(ValueError) as info:
        to_library_name(3.14)
    assert str(info.value) == "Cannot convert nil or non-string class name '3.14' to library name."


def test_boolean():
    with pytest.raises(ValueError) as info:
        to_library_name(True)
    assert str(info.value) == "Cannot convert nil or non-string class name 'True' to library name."


def test_list():
    with pytest.raises(ValueError) as info:
        to_library_name(["AbcXyz"])
    assert str(info.value) == "Cannot convert nil or non-string class name '['AbcXyz']' to library name."
