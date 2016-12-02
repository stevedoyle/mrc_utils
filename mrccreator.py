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
    def __init__(self):
        self.sm = {
            'SINGLE_STEP': self.parse_single_step,
            'REPEAT_BLOCK': self.parse_repeat_block
        }
        self.cur_state = 'SINGLE_STEP'
        self.steps = []
        self.repeat_count = 0
        self.torepeat = []

    def parse(self, line):
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

def parse_workout(workout):
    parser = WorkoutParser()

    steps = []
    lines = [line.lower() for line in workout.split('\n') if line]
    for line in lines:
        if re.search('^#', line):
            continue
        parser.parse(line)
    return parser.steps

def body_line(start, percent):
    return "%0.2f\t%d\n" % (start, percent)

def body_block(start, duration, start_zone, end_zone):
    body = ''
    body += body_line(start, zone_to_percent[start_zone])
    body += body_line(start+duration, zone_to_percent[end_zone])
    return body

def generate_mrc_body(workout):
    steps = parse_workout(workout)

    body = ''
    start = 0
    for step in steps:
        duration = float(step[0])
        if range_to_zones.has_key(step[1]):
            zones = range_to_zones[step[1]]
            body += body_block(start, duration, zones[0], zones[1])
            start += duration
        else:
            body += body_block(start, duration, step[1], step[1])
            start += duration
    return body

def generate_mrc(name, workout):
    body = ''
    body += mrc_header
    body += generate_mrc_body(workout)
    body += mrc_trailer
    return body

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

