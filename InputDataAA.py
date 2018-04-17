###THIS IS THE INPUT DATA#######
# simulation settings
POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 50   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DELTA_T = 1         # years (length of time step, how frequently you look at the patient)
DISCOUNT = 0.03     # annual discount rate

# transition matrix
Q3_TRANS_MATRIX = [
    [0.75,  0.15,   0.0,    0.1],   # Well
    [0,     0.0,    1.0,    0.0],   # Stroke
    [0,     0.25,   0.55,   0.2],   # Post-Stroke
    [0.0,   0.0,    0.0,    1.0],   # Dead
    ]

# utilities
ANNUAL_STATE_UTILITY = [
    1,       # Well
    0.8865,  # Stroke
    0.9,    # Post-Stroke
    0        # Dead
    ]

#costs
ANNUAL_STATE_COST = [
    0,     # Well
    5000,  # Stroke
    200,   # Post-Stroke
    0      # Dead
    ]
#RR of death in stroke
RR_STROKE = 0.65
# anticoag RR
RR_BLEEDING = 1.05

# drug price
anticoagulation_COST = 2000.0
