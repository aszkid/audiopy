"""This file is part of AudioPy.

AudioPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AudioPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AudioPy.  If not, see <http://www.gnu.org/licenses/>."""

import unittest as ut

import audiopy as ap

class read_various(ut.TestCase):
    def setUp(self):
        pass

    def test1(self):
        mybuff = ap.buffer()
        self.assertRaises(IOError, mybuff.read_file, "tests/fakefile.wav")

if __name__ == "__main__":
    ut.main()
