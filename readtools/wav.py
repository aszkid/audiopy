import numpy as np
import logging
log = logging.getLogger("ap.rtools.wav")

# Thanks to 'WarrenWeckesser': https://gist.github.com/WarrenWeckesser/7461781

def bytes_to_array(par, data):
    if par["sampwidth"] == 3:
        # adapt sample width for 24b samples
        pass
    else:
        ch = 'u' if par["sampwidth"] == 1 else 'i'
        a = np.fromstring(data, dtype='<{0}{1}'.format(ch, par["sampwidth"]))
        result = a.reshape(-1, par["nchannels"])
    
    return result
