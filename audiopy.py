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

import wave
import struct
import logging
logging.basicConfig()
log = logging.getLogger("ap")

from readtools import wav

WAV     = 1
FLAC    = 2
MP3     = 3

formats = [
    WAV, FLAC, MP3
]

formats_ext = {
    "wav"   : WAV,
    "flac"  : FLAC,
    "mp3"   : MP3
}

def guess_format_ext(name):
    ext = name.split('.')[-1].lower()
    if ext in formats_ext:
        return formats_ext[ext]
    else:
        return None
def guess_format_dat(file):
    # try to do this somehow
    return None

class buffer:

    def __init__(self):
	    self.data = None
	    self.format = None
	    
	    self.prop = {
	        "nchannels" : None,
	        "framerate" : None,
	        "nframes"   : None,
	        "sampwidth" : None
	    }
    
    def frame_count(self, t):
        return self.prop["framerate"] * t
    
    def write_file(self, filename):
        try:
            file = open(filename, 'wb')
        except IOError:
            raise
        
        if self.format == WAV:
            
            wobj = wave.open(file)
            wtup = (self.prop["nchannels"], self.prop["sampwidth"],
                self.prop["framerate"], self.prop["nframes"],
                'NONE', 'not compressed')
            wobj.setparams(wtup)
            
            chunk_s = 4096
            chunk = [None]*(chunk_s*self.prop["nchannels"])
            chunk_c, rem = divmod(self.prop["nframes"], chunk_s)
            log.debug("writing %i chunks of %i frames + %i remaining frames", chunk_c, chunk_s, rem)
            
            ch = 'c' if self.prop["sampwidth"] == 1 else 'h'
            form = '<{0}'.format(ch)
            
            """for chunk_i in xrange(0, chunk_c):
                for frame_i in xrange(0, chunk_s):
                    i = chunk_i * chunk_s + frame_i
                    for chann_i in xrange(0, self.prop["nchannels"]):
                        chunk[frame_i*2 + chann_i] = struct.pack(form, self.data[i][chann_i])
                wobj.writeframes(''.join(chunk))
            
            chunk = [None]*(rem*self.prop["nchannels"])
            for frame_i in xrange(0, rem):
                i = chunk_c * chunk_s + frame_i
                for chann_i in xrange(0, self.prop["nchannels"]):
                        chunk[frame_i*2 + chann_i] = struct.pack(form, self.data[i][chann_i])
            wobj.writeframes(''.join(chunk))"""
            
            buff = [None]*(self.prop["nframes"]*self.prop["nchannels"])
            
            for fi in xrange(0, self.prop["nframes"]):
                for ci in xrange(0, self.prop["nchannels"]):
                    buff[fi*2+ci] = struct.pack(form, self.data[fi][ci])
            wobj.writeframes(''.join(buff))
            
        elif self.format == FLAC:
            pass
        elif self.format == MP3:
           pass
        else:
            pass
        
    def read_file(self, filename, format=None):
        file = None
        
        try:
            file = open(filename, 'rb')
        except IOError:
            raise

        if format in formats:
            self.format = format
        else:
            self.format = guess_format_ext(filename)
        if self.format == None:
            self.format = guess_format_dat(file)
        if self.format == None:
            raise Exception("Could not guess file format.")
                
        log.debug("Opened file '%s', format '%i'.", filename, self.format)
        
        if self.format == WAV:
            try:
                wobj = wave.open(file)
                wtup = wobj.getparams()
                
                self.prop["nchannels"]    = wtup[0]
                self.prop["sampwidth"]    = wtup[1]
                self.prop["framerate"]    = wtup[2]
                self.prop["nframes"]      = wtup[3]
                self.prop["duration"]     = self.prop["nframes"] / float(self.prop["framerate"])
                
                fdata = wobj.readframes(self.prop["nframes"])
                self.data = wav.bytes_to_array(self.prop, fdata)
                
            except wave.Error:
                raise
        elif self.format == FLAC:
            pass
        elif self.format == MP3:
            pass
        else:
            pass
            
        log.debug(self.prop)
        
