# if this doesn't work: http://freemusicarchive.org/music/James_Kibbie/Bach_Organ_Works_Individual_Chorale_Preludes/BWV0668
# ----
wget http://freemusicarchive.org/music/download/50217836fb9607edf4bca5a8a4c669bd2dfcdfad -q -O tests/full_bach.mp3
ffmpeg -i tests/full_bach.mp3 tests/full_bach.wav
rm tests/full_bach.mp3
