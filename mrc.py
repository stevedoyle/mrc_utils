#!/usr/bin/env python

import re
import sys
import argparse
import logging

mrc_header = """[COURSE HEADER]
VERSION = 2
UNITS = ENGLISH
DESCRIPTION = Sample
FILE NAME = sample.mrc
MINUTES PERCENT
[END COURSE HEADER]
[COURSE DATA]
"""

mrc_trailer = """[END COURSE DATA]"""

zone_to_percent = {
    'lz1':45, 'z1':50, 'hz1':55,
    'lz2':58, 'z2':65, 'hz2':73,
    'lz3':78, 'z3':82, 'hz3':88,
    'lz4':93, 'z4':98, 'hz4':103,
    'lz5':107, 'z5':108, 'hz5':118,
    'z5+':130, 'max':150
    }

range_to_zones = {
    'z1>z2':('z1','z2'),
    'z1>z3':('z1','z3'),
    'z1>z4':('z1','z4'),
    'z2>z1':('z2','z1'),
    'z3>z1':('z3','z1')
    }

class WorkoutParser:
    def __init__(self, workout):
        self.workout = workout
        self.sm = {
            'SINGLE_STEP': self.parse_single_step,
            'REPEAT_BLOCK': self.parse_repeat_block
        }
        self.cur_state = 'SINGLE_STEP'
        self.steps = []
        self.repeat_count = 0
        self.torepeat = []

    def parse(self):
        lines = [line.lower() for line in self.workout.split('\n') if line]
        for line in lines:
            if re.search('^#', line):
                continue
            self.parseline(line)
        return self.steps

    def parseline(self, line):
        self.sm[self.cur_state](line)

    def parse_single_step(self, line):
        mobj = re.search('repeat\s+([\d]+):', line)
        if mobj:
            self.repeat_count = int(mobj.group(1))
            self.cur_state = 'REPEAT_BLOCK'
            return

        mobj = re.search('^([\d.]+)\s+([\w><]+)', line)
        if mobj:
            self.steps.append((mobj.group(1), mobj.group(2)))

    def parse_repeat_block(self, line):
        mobj = re.search('\s+([\d.]+)\s+([\w><]+)', line)
        if mobj:
            self.torepeat.append((mobj.group(1), mobj.group(2)))
            return

        mobj = re.search('^([\d.]+)\s+([\w><]+)', line)
        if mobj:
            self.insert_repeat_steps()
            self.cur_state = 'SINGLE_STEP'
            self.parse_single_step(line)

    def insert_repeat_steps(self):
        self.steps += self.torepeat * self.repeat_count
        self.torepeat = []
        self.repeat_count = 0

class MrcGenerator:
    def __init__(self, workout):
        self.body = ''
        self.workout = workout

    def generate(self, workout):
        self.generate_header()
        self.generate_body()
        self.generate_trailer()
        return self.body

    def generate_header(self):
        self.body += mrc_header

    def generate_trailer(self):
        self.body += mrc_trailer

    def generate_body(self):
        start = 0
        for step in self.workout:
            duration = float(step[0])
            if range_to_zones.has_key(step[1]):
                zones = range_to_zones[step[1]]
                self.body_block(start, duration, zones[0], zones[1])
                start += duration
            else:
                self.body_block(start, duration, step[1], step[1])
                start += duration

    def body_line(self, start, percent):
        return "%0.2f\t%d\n" % (start, percent)

    def body_block(self, start, duration, start_zone, end_zone):
        self.body += self.body_line(start, zone_to_percent[start_zone])
        self.body += self.body_line(start+duration, zone_to_percent[end_zone])

def generate_mrc(name, workout):
    p = WorkoutParser(workout)
    g = MrcGenerator(p.parse())
    return g.generate(workout)

def main():
    parser = argparse.ArgumentParser(description="MRC File Generator")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Verbose output")
    parser.add_argument('workout', type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    mrc = generate_mrc('Sample', args.workout.read())
    print mrc

if __name__ == "__main__":
    main()

