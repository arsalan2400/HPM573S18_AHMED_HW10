#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 13:39:58 2018

@author: Aslan
"""

###HOMEWORK QUESTION 2######

import ParameterClassesAA as P
import MarkovModelClassesAA as MarkovCls
import SupportMarkovModel as SupportMarkov
import SamplePathClasses as PathCls
import FigureSupport as Figs

# create none and cohort
a_cohort_without_therapy = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)
simOutputs_NONE = a_cohort_without_therapy.simulate()

# create anti and cohort
a_cohort_with_anticoag_therapy = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)
simOutputs_ANTICOAG = a_cohort_with_anticoag_therapy.simulate()


###Grab it from SupportMarkov model.
SupportMarkov.print_comparative_outcomes(simOutputs_NONE, simOutputs_ANTICOAG)

