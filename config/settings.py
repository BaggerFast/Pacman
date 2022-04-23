import os
import sys
from typing import NamedTuple

VERSION = '1.0.3'
DEBUG = 'debug' in sys.argv


class Dir(NamedTuple):
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSET = os.path.join(BASE, 'assets')
    IMAGE = os.path.join(ASSET, 'images')
    SOUND = os.path.join(ASSET, 'sounds')
