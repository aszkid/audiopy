import numpy as np
import logging
log = logging.getLogger("ap.iotools.wav")
import wave
import struct

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
                
