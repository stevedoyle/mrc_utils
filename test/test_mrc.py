import unittest
import mrc

class WorkoutParserTest(unittest.TestCase):
    def test_single_step(self):
        workout = '10 z1'
        steps = mrc.WorkoutParser(workout).parse()
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps, [('10', 'z1')])

    def test_multiple_steps(self):
        workout = '10 z1\n5 z2'
        steps = mrc.WorkoutParser(workout).parse()
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps, [('10', 'z1'), ('5', 'z2')])

    def test_zone_ramp(self):
        workout = '10 z1>z3'
        steps = mrc.WorkoutParser(workout).parse()
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps, [('10', 'z1>z3')])
        pass

    def test_legal_zones(self):
        pass

    def test_illegal_zones(self):
        pass

    def test_case_tolerance(self):
        workout = '10 Z1'
        steps = mrc.WorkoutParser(workout).parse()
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps, [('10', 'z1')])

    def test_repeat_block(self):
        pass

