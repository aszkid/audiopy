import logging
logging.getLogger("ap").setLevel(logging.DEBUG)

import audiopy as ap

buff = ap.buffer()
buff.read_file("tests/full_bach.wav")

import pylab as p
import time

t1 = buff.frame_count(0)
t2 = buff.frame_count(10)
p.plot(buff.data[t1:t2, 0])
p.plot(buff.data[t1:t2, 1])
p.savefig("{0}.png".format(time.time()))

buff.write_file("tests/full_bach_re.wav")
