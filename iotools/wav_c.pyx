import struct

def _populate_chunk(fbeg, fend, indexbeg, chbeg, chend, prop, enc, data, chunk):
    chind = (chend-chbeg)
    for frame_i in xrange(fbeg, fend):
        i = indexbeg + frame_i
        for chann_i in xrange(chbeg, chend):
            chunk[frame_i*chind + chann_i] = struct.pack(enc, data[i][chann_i])
