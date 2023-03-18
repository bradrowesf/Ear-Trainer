"""Test module"""
import random

from scamp import Session


def hello_world():
    """Core function"""
    sess = Session()
    clarinet = sess.new_part("Clarinet")
    scale = [60, 62, 64, 65, 67, 69, 71]
    count = 0
    while count < 10:
        note = random.choice(scale)
        clarinet.play_note(note, 0.8, 2)
        count += 1


hello_world()
