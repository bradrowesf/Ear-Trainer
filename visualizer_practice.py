'''Let's practice visualizing this data'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from src.scorehistory import ScoreHistory


sc = ScoreHistory()
df = sc.get_dataframe()

unique_tests = df[0].unique()
unique_testgroups = []
for unique_test in unique_tests:
    test_split = unique_test.split(':')
    test_groupname = test_split[0]
    if test_groupname in unique_testgroups:
        continue
    unique_testgroups.append(test_groupname)

print(unique_testgroups)

'''subset1 = df[df[0] == 'Singing the Easy Intervals:m3']
subset2 = df[df[0] == 'Singing the Easy Intervals:-m3']
subset3 = df[df[0] == 'Singing the Medium Intervals:M6']

fig, ax = plt.subplots()
subset1.plot.line(ax=ax, x=2, y=1, marker='o')
subset2.plot.line(ax=ax, x=2, y=1, marker='o')
subset3.plot.line(ax=ax, x=2, y=1, marker='o')

plt.show()'''
