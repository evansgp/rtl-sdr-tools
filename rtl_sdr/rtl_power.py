from math import ceil
import sys
import csv

class Readings:
    """Represents a set of readings from rtl_power"""

    def __init__(self, hz_low, hz_high, hz_step, n_steps, data):
        self.hz_low = hz_low
        self.hz_high = hz_high
        self.hz_step = hz_step
        self.n_steps = n_steps
        self.data = data
        if ceil((self.hz_high - self.hz_low) / self.hz_step) != self.n_steps:
            raise Exception('step size did not segment freq range into number of steps')

class Parser:
    """Parses rtl_power CSV entries into objects"""

    _field_names = ['date', 'time', 'low', 'high', 'step', 'n']
    _rest_key = 'samples'

    def __init__(self, file):
        self.file = file
        self.blocks = csv.DictReader(self.file, fieldnames=self._field_names, restkey=self._rest_key, skipinitialspace=True)

    def readings(self):
        last = next(self.blocks)
        hz_low = float(last['low'])
        hz_step = float(last['step'])
        data = [last['samples']]
        for block in self.blocks:
            if self.id(block) == self.id(last):
                target = data[-1]
            else:
                target = data
            target.append(block['samples'])
            last = block
        n_steps = len(data[0])
        hz_high = hz_low + hz_step * n_steps
        return Readings(hz_low, hz_high, hz_step, n_steps, data)

    def id(self, block):
        return (block['date'], block['time'])
