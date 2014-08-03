import logging
logging.getLogger("ap").setLevel(logging.DEBUG)

import audiopy as ap

buff = ap.buffer()
buff.read_file("tests/full_bach.wav")
buff.write_file("tests/full_bach_re.wav")
