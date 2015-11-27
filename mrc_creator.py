#!/usr/bin/env python

import re
import sys
import argparse

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

def parse_workout(workout):
    steps = []
    lines = [line.strip() for line in workout.split('\n') if line]
    for line in lines:
        if re.search('^#', line):
            continue
        mobj = re.search('^([\d.]+)\s+([\w><]+)', line)
        if mobj:
            steps.append((mobj.group(1), mobj.group(2)))
    return steps

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
    parser.add_argument('workout', type=argparse.FileType('r'))

    args = parser.parse_args()
    mrc = generate_mrc('Sample', args.workout.read())
    print mrc

if __name__ == "__main__":
    main()

