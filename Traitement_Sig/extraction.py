import numpy as np
from scipy import signal
from scipy.io import wavfile
from os.path import dirname, join as pjoin

class Extractor:

    def __init__(self, filename=None):
        self.filename = filename
        self.sample_rate = None
        self.data = None
        if filename is not None:
            self.read(self.filename)

    def read(self, filename):
        self.sample_rate, self.data = wavfile.read(filename)

    def __getitem__(self, item):
        return self.sample_rate, self.data

    def extract_param(self, note, sample_rate=None):
        if sample_rate is None:
            sample_rate = self.sample_rate

    