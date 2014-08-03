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

import numpy as np
import logging
log = logging.getLogger("ap.iotools.wav")
import wave

import misc
import wav_c

def read(file, prop):
    wobj = wave.open(file)
    wtup = wobj.getparams()
    
    prop["nchannels"]    = wtup[0]
    prop["sampwidth"]    = wtup[1]
    prop["framerate"]    = wtup[2]
    prop["nframes"]      = wtup[3]
    prop["duration"]     = prop["nframes"] / float(prop["framerate"])
    
    fdata = wobj.readframes(prop["nframes"])
    data = misc.bytes_to_array(prop, fdata)

    return (data, prop)

def write(file, prop, data):
    wobj = wave.open(file)
    wtup = (prop["nchannels"], prop["sampwidth"],
        prop["framerate"], prop["nframes"],
        'NONE', 'not compressed')
    wobj.setparams(wtup)
    
    chunk_s = 16384
    chunk_c, rem = divmod(prop["nframes"], chunk_s)
    log.debug("writing %i chunks of %i frames + %i remaining frames", chunk_c, chunk_s, rem)
    
    ch = 'c' if prop["sampwidth"] == 1 else 'h'
    form = '<{0}'.format(ch)
    
    wav_c.write_chunks(chunk_c, chunk_s, rem, form, data, prop, wobj)
                
