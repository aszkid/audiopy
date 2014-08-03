import numpy as np
import logging
log = logging.getLogger("ap.rtools.wav")
import wave
import struct

import misc

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

def _populate_chunk(fbeg, fend, indexbeg, chbeg, chend, prop, enc, data, chunk):
    chind = (chend-chbeg)
    for frame_i in xrange(fbeg, fend):
        i = indexbeg + frame_i
        for chann_i in xrange(chbeg, chend):
            chunk[frame_i*chind + chann_i] = struct.pack(enc, data[i][chann_i])

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
        _populate_chunk(0, chunk_s, chunk_i*chunk_s, 0, prop["nchannels"], prop, form, data, chunk)
        wobj.writeframes(''.join(chunk))
    
    chunk = [None]*(rem*prop["nchannels"])
    _populate_chunk(0, rem, chunk_c*chunk_s, 0, prop["nchannels"], prop, form, data, chunk)
    wobj.writeframes(''.join(chunk))
                
