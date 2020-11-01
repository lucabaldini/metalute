# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Pitch-related facilities.
"""

A4_FREQ = 440.


class ScientificPitchNotation:

    """Implementation of the scientific pitch notattion, see
    https://en.wikipedia.org/wiki/Scientific_pitch_notation
    """

    __NOTE_DICT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    __START_OCTAVE = -1
    __ACCIDENTAL_DICT = {'b': -1, '#': 1}
    __ACCIDENTALS = tuple(__ACCIDENTAL_DICT.keys())
    SEMITONES_PER_OCTAVE = 12

    @classmethod
    def note_number(self, note):
        """Return the note number for a given note in scientific pitch notation.
        """
        number = self.__NOTE_DICT[note[0]]
        try:
            number += self.__ACCIDENTAL_DICT[note[1]]
            octave = int(note[2:])
        except KeyError:
            octave = int(note[1:])
        number += self.SEMITONES_PER_OCTAVE * (octave - self.__START_OCTAVE)
        return number

    @classmethod
    def frequency(self, note):
        """Return the frequency for a given note.
        """
        if isinstance(note, str):
            note = self.note_number(note)
        return A4_FREQ * 2.**((note - 69.) / 12.)


if __name__ == '__main__':
    print(ScientificPitchNotation.note_number('A4'))
    print(ScientificPitchNotation.frequency('A4'))
    print(ScientificPitchNotation.frequency(69))
    print(ScientificPitchNotation.frequency(69.5))
    print(ScientificPitchNotation.frequency(70.))
