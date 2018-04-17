#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tues Apr 16 12:08:42 2018
@author: Aslan
"""

import InputData as Settings
import FormatFunctions as F
import SamplePathClasses as PathCls
import FigureSupport as Figs
import StatisticalClasses as Stat
import EconEvalClassesAA as Econ


def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)
 
    # mean and confidence interval text of times of stroke
    strokes_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_count_strokes().get_mean(),
        interval=simOutput.get_sumStat_count_strokes().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_cost().get_mean(),
        interval=simOutput.get_sumStat_discounted_cost().get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_utility().get_mean(),
        interval=simOutput.get_sumStat_discounted_utility().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean time to AIDS and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          strokes_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def draw_survival_curves_and_histograms(simOutputs_NONE, simOutputs_ANTICOAG):
    """ draws the survival curves and the histograms of time until HIV deaths
    :param simOutputs_NONE: output of a cohort simulated under no therapy
    :param simOutputs_ANTICOAG: output of a cohort simulated under anticoag therapy
    """

    # get survival curves of both treatments
    survival_curves = [
        simOutputs_NONE.get_survival_curve(),
        simOutputs_ANTICOAG.get_survival_curve()
    ]

    # graph survival curve
    PathCls.graph_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=['No Therapy Present', 'Anticoagulation Therapy Present']
    )

    # histograms of survival times
    set_of_survival_times = [
        simOutputs_NONE.get_survival_times(),
        simOutputs_ANTICOAG.get_survival_times()
    ]

    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_survival_times,
        title='Histogram of patient survival time',
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legends=['No Therapy Present', 'Anticoagulation Therapy Present'],
        transparency=0.6
    )


def print_comparative_outcomes(simOutputs_NONE, simOutputs_ANTICOAG):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under anti therapy compared to no therapy
    :param simOutputs_NONE: output of a cohort simulated under no therapy
    :param simOutputs_ANTICOAG: output of a cohort simulated under anticoag therapy
    """

    # increase in survival time under combination therapy with respect to no therapy
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in survival time',
        x=simOutputs_ANTICOAG.get_survival_times(),
        y_ref=simOutputs_NONE.get_survival_times())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_survival_time.get_mean(),
        interval=increase_survival_time.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in survival time "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)
   
    
    ###NEW STUFF TO ADD IN######
    
    # increase in stroke # under combination therapy with respect to none therapy
    increase_strokecount  = Stat.DifferenceStatIndp(
        name='Increase in the Expected Number of Strokes',
        x=simOutputs_ANTICOAG.get_if_developed_stroke(),
        y_ref=simOutputs_NONE.get_if_developed_stroke())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_strokecount.get_mean(),
        interval=increase_strokecount.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in stroke count # is...."
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)
       
    
    # increase in discounted total cost under combination therapy with respect to no therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in discounted cost with Anticoagulation Therapy',
        x=simOutputs_NONE.get_costs(),
        y_ref=simOutputs_ANTICOAG.get_costs())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_cost.get_mean(),
        interval=increase_discounted_cost.get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)
    print("Average increase in discounted cost is..."
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # increase in discounted total utility under combination therapy with respect to no therapy
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_NONE.get_utilities(),
        y_ref=simOutputs_ANTICOAG.get_utilities())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_utility.get_mean(),
        interval=increase_discounted_utility.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in discounted utility is... "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)



def report_CEA_CBA(simOutputs_NONE, simOutputs_ANTICOAG):
    """ performs cost-effectiveness analysis
    :param simOutputs_none: output of a cohort simulated under no therapy
    :param simOutputs_ANTICOAG: output of a cohort simulated under anticoag therapy
    """

    # define two strategies
    NONE_therapy_strategy = Econ.Strategy(
        name='No Therapy',
        cost_obs=simOutputs_NONE.get_costs(),
        effect_obs=simOutputs_NONE.get_utilities()
    )
    
    ANTICOAG_therapy_strategy = Econ.Strategy(
        name='Anticoag Therapy',
        cost_obs=simOutputs_ANTICOAG.get_costs(),
        effect_obs=simOutputs_ANTICOAG.get_utilities()
    )

    # CEA
    CEA = Econ.CEA(
        strategies=[NONE_therapy_strategy, ANTICOAG_therapy_strategy],
        if_paired=False
    )
    
    
    ###THIS IS THE SAME FROM SUPPORTMARKOV.pY in class######
    # show the CE plane
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )

    # CBA
    NBA = Econ.CBA(
        strategies=[NONE_therapy_strategy, ANTICOAG_therapy_strategy],
        if_paired=False
    )
    
    # show the net monetary benefit figure
    NBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval=Econ.Interval.CONFIDENCE,
        show_legend=True,
        figure_size=6
    )
