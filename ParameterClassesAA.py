#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 06:01:36 2018

@author: Aslan
"""

from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputDataAA as INPUT
import MarkovModelClassesAA as MarkovCls
import RandomVariantGenerators as Random
import ProbDistParEstAA as Est

###First thing we need to do is set our healthstats and therapies. 
class HealthStats(Enum):
    WELL = 0
    STROKE= 1
    POST_STROKE= 2
    DEATH = 3

class Therapies(Enum):
    NONE = 0
    ANTICOAG = 1

####note that the matrices are labelled based on the input.Q3_TRANS_MATRIX
    
class ParametersFixed():
    def __init__(self, drug):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = INPUT.DELTA_T
        
        # Identify the initial health state, which is WELL. 
        self._initialHealthState = HealthStats.WELL
       
        # transition probability matrix of the selected therapy
        self._prob_matrix =[] ### We dont' haev an updated matrix this time!
###Add this####
        self._treatmentRR = 0

        # calculate transition probabilities and treatment cost depending of which therapy options is in use
        if therapy == Therapies.NONE:
            self._prob_matrix = INPUT.Q3_TRANS_MATRIX
            self._annualTreatmentCost = 0
        else:
            self._prob_matrix = calculate_prob_matrix_anticoag()
            self._annualTreatmentCost = INPUT.anticoagulation_COST

        # annual state costs and utilities
        self._annualStateCosts = INPUT.ANNUAL_STATE_COST
        self._annualStateUtilities = INPUT.ANNUAL_STATE_UTILITY

###This is just the relevant functions I pick out from ParameterClasses.py on the class list
##Toss these in!!### Only really need adjDiscountRate I think....
    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate
    
    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost


###We need to find this. Note that I use INPUT. instead of data. in my inputs####

def calculate_prob_matrix_anticoag():
    """ :returns transition probability matrix under anticoagulation use"""

    # create an empty matrix populated with zeroes
    prob_matrix = []
    for s in HealthStats:
        prob_matrix.append([0] * len(HealthStats))

    # for all health states
    for s in HealthStats:
        # if the current state is post-stroke
        if s == HealthStats.POST_STROKE:
            # post-stoke to stroke
            prob_matrix[s.value][HealthStats.STROKE.value]\
                = INPUT.RR_STROKE * INPUT.Q3_TRANS_MATRIX[s.value][HealthStats.STROKE.value]
            # post-stroke to death
            prob_matrix[s.value][HealthStats.DEATH.value] \
                = INPUT.RR_STROKE * INPUT.RR_BLEEDING * INPUT.Q3_TRANS_MATRIX[s.value][HealthStats.DEATH.value]
            # staying in post-stroke
            prob_matrix[s.value][s.value]\
                = 1 -prob_matrix[s.value][HealthStats.STROKE.value] -prob_matrix[s.value][HealthStats.DEATH.value]
        else:
            prob_matrix[s.value] = INPUT.Q3_TRANS_MATRIX[s.value]

    return prob_matrix