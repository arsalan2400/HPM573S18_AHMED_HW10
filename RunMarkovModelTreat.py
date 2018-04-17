#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:28:57 2018

@author: Aslan
"""

import ParameterClassesAA as P
import MarkovModelClassesAA as MarkovCls
import SupportMarkovModel as SupportMarkov
import SamplePathClasses as PathCls
import FigureSupport as Figs

# create and simulate cohort
cohort = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)

simOutputs = cohort.simulate()

# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs.get_survival_curve(),
    title='Survival curve',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )

# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs.get_survival_times(),
    title='Survival times of patients with Stroke',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=1
)

# graph histogram of number of strokes
Figs.graph_histogram(
    data=simOutputs.get_if_developed_stroke(),
    title='Number of Strokes per Patient',
    x_label='Stroke Times',
    y_label='Count',
    bin_width=1
)

SupportMarkov.print_outcomes(simOutputs, 'Treatment outcomes are....:')
