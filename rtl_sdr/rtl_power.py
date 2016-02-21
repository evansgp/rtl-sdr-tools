from math import ceil
from datetime import datetime, timezone
import csv

#TODO move from tuples to classes or dicts
#TODO make async, able to stream continuously, use generators(?)
#TODO is the ~2Hz bin error my fault or rtl_power's?
#TODO can the 'samples' column be used for anything?

class Readings:
    """Represents a set of readings from rtl_power"""

    def __init__(self):
        self.spectrum = [] # [(t, [(f, db), ...]), ...]

    def add(self, time_row):
        if self.spectrum and self.spectrum[-1][0] >= time_row[0]:
            raise Exception('new time {} was not after previous {}', time_row[0], self.spectrum[-1][0])
        self.spectrum.append(time_row)

class Parser:
    """Parses rtl_power CSV entries into objects"""

    _field_names = ['date', 'time', 'low', 'high', 'step', 'samples']
    _rest_key = 'bins'
    _ts_format = '%Y-%m-%d%H:%M:%S'

    def __init__(self, file):
        self._file = file
        self._blocks = csv.DictReader(self._file, fieldnames=self._field_names, restkey=self._rest_key, skipinitialspace=True)
        self.readings = Readings()
        self._current = (datetime.min.replace(tzinfo=timezone.utc), []) # (t, [(f, db), ...])

    def process(self):
        for block in self._blocks:
            (freq_low, freq_high, freq_step, ts, bins) = self._parse(block)
            self._validate(freq_low, freq_high, freq_step, len(bins))
            freq = freq_low # starting position
            for db in bins:
                # track freq as a float but output as int
                self._add(ts, int(freq), db)
                freq += freq_step

    def _parse(self, block):
        freq_low = int(block['low'])
        freq_high = int(block['high'])
        freq_step = float(block['step'])
        ts = datetime.strptime(block['date'] + block['time'], self._ts_format).replace(tzinfo=timezone.utc)
        bins = [float(b) for b in block['bins']]
        return (freq_low, freq_high, freq_step, ts, bins)

    def _validate(self, freq_low, freq_high, freq_step, actual_bins):
        expected_bins = ceil((freq_high + freq_step - freq_low) / freq_step)
        if expected_bins != actual_bins:
            raise Exception('expected {} bins, got {}: freq_high = {}, freq_low = {}, freq_step = {}'
                .format(expected_bins, actual_bins, freq_high, freq_low, freq_step))

    def _add(self, ts, freq, db):
        if self._current[0] > ts:
            raise Exception('block stream was not time ordered')
        elif self._current[0] != ts:
            if self._current[1]: # don't emit rows with no data
                self.readings.add(self._current)
            self._current = (ts, [])
        self._current[1].append((freq, db))
