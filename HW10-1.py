#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:35:20 2018

@author: Aslan
"""

import ParameterClassesAA as P
import MarkovModelClassesAA as MarkovCls
import SupportMarkovModel as SupportMarkov
import SamplePathClasses as PathCls
import FigureSupport as Figs

# create and cohort
a_cohort_without_therapy = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)
simOutputs_NONE = a_cohort_without_therapy.simulate()


# create and cohort
a_cohort_with_anticoag_therapy = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)
simOutputs_ANTICOAG = a_cohort_with_anticoag_therapy.simulate()

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs_NONE, 'No treatment outcomes are...:')

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs_ANTICOAG, 'Anticoagulation treatment outcomes are...:')

