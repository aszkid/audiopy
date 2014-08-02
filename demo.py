import logging
logging.getLogger("ap").setLevel(logging.DEBUG)

import audiopy as ap

buff = ap.buffer()
buff.read_file("tests/test.wav")

import pylab as p
p.plot(buff.data)
p.show()
