# module wis.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
wis module - Functions to solve de Weight Interval Schedule problem

The core function is schedule, which receives an array of Task as argument.
It uses a dynamic programming aproach in order to solve the problem (if 
we assume that the tasks are ordered by end time).
"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

from collections import namedtuple

Task = namedtuple('Task', 'start end weight index')

def schedule(tasks):
    """Schedule compatible tasks with maximum weight.

    Args:
        tasks: Array of Task
    Returns:
        A tuple composed by the Maximum weight found
        and the set of compatible tasks.
    """
    tasks = sortTasksByEnd(tasks)
    tasks.insert(0, Task(0,0,0))

    num_tasks = len(tasks)
    p = createPreviousArray(tasks)

    max_w = [0]
    set_tasks = [[]]

    for i in range(num_tasks)[1:]:
        if tasks[i].weight + max_w[ p[i] ] >= max_w[i - 1]:
            max_w.append( tasks[i].weight + max_w[ p[i] ] )
            set_tasks.append( set_tasks[ p[i] ] + [tasks[i]] )
        else:
            max_w.append( max_w[i - 1] )
            set_tasks.append( set_tasks[i-1] )

    return max_w[num_tasks-1], set_tasks[num_tasks-1]

def sortTasksByEnd(tasks):
    return sorted(tasks, key=lambda task: task.end)

def createPreviousArray(tasks):
    num_tasks = len(tasks)
    return [ previous(i, tasks) for i in range(num_tasks) ]

def previous(i, tasks):
    if i == 1 or i == 0:
        return 0
    else:
        j = i
        while j > 1:
            j = j - 1
            if tasks[j].end <= tasks[i].start:
                return j
        return 0