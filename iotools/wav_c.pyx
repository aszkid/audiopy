import struct

def _populate_chunk(int fbeg, int fend, int indexbeg, int chbeg, int chend, prop, enc, data, chunk):
    cdef int chind = (chend-chbeg)
    cdef int i, fcind
    for frame_i from fbeg <= frame_i < fend:
        i = indexbeg + frame_i
        fcind = frame_i*chind
        for chann_i from chbeg <= chann_i < chend:
            chunk[fcind + chann_i] = struct.pack(enc, data[i][chann_i])
