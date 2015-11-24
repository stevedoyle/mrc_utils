# mrc_utils
[TrainerRoad](http://trainerroad.com) allows workouts to be created by [importing ERG and MRC files](http://support.trainerroad.com/hc/en-us/articles/201944204-Creating-a-Workout-from-an-ERG-or-MRC-File).
These utilities allow the creation of an MRC file based on a higher level language for specifying the workout.

For example, using the following workout as an input in the file sample.in:

```
15 z1>z3
1  z4
4  z1
1  hz4
1  z1
2  hz4
2  z1
3  hz4
3  z1
4  hz4
4  z1
3  z5
3  z1
2  z5
2  z1
1  z5
1  z1
20 z2>z1
```

`mrc_creator.py sample.in`

Output (suitable for import into TrainerRoad):

```
[COURSE HEADER]
VERSION = 2
UNITS = ENGLISH
DESCRIPTION = HIIT Pyramid
FILE NAME = hiit_pyramid.mrc
MINUTES PERCENT
[END COURSE HEADER]
[COURSE DATA]
0.00	40
15.00	90
15.00	100
16.00	100
16.00	50
20.00	50
20.00	103
21.00	103
21.00	50
22.00	50
22.00	103
24.00	103
24.00	50
26.00	50
26.00	103
29.00	103
29.00	50
32.00	50
32.00	103
36.00	103
36.00	50
40.00	50
40.00	115
43.00	115
43.00	50
46.00	50
46.00	115
48.00	115
48.00	50
50.00	50
50.00	115
51.00	115
51.00	50
52.00	50
52.00	75
72.00	45
[END COURSE DATA]
```

