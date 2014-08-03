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
    chunk = [None]*(chunk_s*prop["nchannels"])
    chunk_c, rem = divmod(prop["nframes"], chunk_s)
    log.debug("writing %i chunks of %i frames + %i remaining frames", chunk_c, chunk_s, rem)
    
    ch = 'c' if prop["sampwidth"] == 1 else 'h'
    form = '<{0}'.format(ch)
    
    for chunk_i in xrange(0, chunk_c):
        wav_c._populate_chunk(0, chunk_s, chunk_i*chunk_s, 0, prop["nchannels"], prop, form, data, chunk)
        wobj.writeframes(''.join(chunk))
    
    chunk = [None]*(rem*prop["nchannels"])
    wav_c._populate_chunk(0, rem, chunk_c*chunk_s, 0, prop["nchannels"], prop, form, data, chunk)
    wobj.writeframes(''.join(chunk))
                
