import logging
logging.getLogger("ap").setLevel(logging.DEBUG)

import audiopy as ap

buff = ap.buffer()
buff.read_file("tests/bach_kibbie.wav")

import pylab as p

t1 = buff.prop["framerate"] * 0
t2 = t1 + buff.prop["framerate"] * 10
p.plot(buff.data[t1:t2, 0])
p.plot(buff.data[t1:t2, 1])
p.show()
