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

import struct
import wave
import numpy as np
cimport numpy as np

def _populate_chunk(int fbeg, int fend, int indexbeg, int chbeg, int chend, data, chunk):
    cdef int chind = (chend-chbeg)
    cdef int i, fcind
    for frame_i from fbeg <= frame_i < fend:
        i = indexbeg + frame_i
        fcind = frame_i*chind
        for chann_i from chbeg <= chann_i < chend:
            chunk[fcind + chann_i] = data[i][chann_i]

def write_chunks(int chunk_c, int chunk_s, int rem, form, data, prop, wobj):        
    cdef int chunk_i
    cdef np.ndarray chunk = np.empty(chunk_s*prop["nchannels"], dtype=form)
    
    for chunk_i from 0 <= chunk_i < chunk_c:
        _populate_chunk(0, chunk_s, chunk_i*chunk_s, 0, prop["nchannels"], data, chunk)
        wobj.writeframes(chunk.tostring())
    
    chunk = np.empty(rem*prop["nchannels"], dtype=form)
    _populate_chunk(0, rem, chunk_c*chunk_s, 0, prop["nchannels"], data, chunk)
    wobj.writeframes(chunk.tostring())
    
