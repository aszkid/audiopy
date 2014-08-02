import audiopy as ap

import logging
logging.getLogger("ap").setLevel(logging.DEBUG)

buff = ap.buffer()
buff.read_file("tests/test.wav")
