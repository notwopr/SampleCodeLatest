"""
Title: Business Model Bot
Version: 1.01
Date Started: Oct 22, 2019
Date Updated: June 25, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Model several different possible business models at once and return results.

Versions:
1.01: Create Master script for readability.
"""
import matplotlib.pyplot as plt
import pandas as pd
from businessmodelbot_base import FundProfile, comp_edge_needed, graph_edgerate, graph_edgerate3d, fundprofiler

'''INPUTS'''
# CLIENT BASE
client_principal = 100  # amount of money one client has to invest
num_clients = 10  # num of clients our fund has
comp_num_clients = 20  # num of clients our competitor has

# REVENUE
perf_cut = 0.5  # the portion of gains client earns that go to us
aum_rate = 0.01  # the fee rate charged by us for managing a client's assets
comp_perf_cut = 0.10  # competitor's performance cut
comp_aum_rate = 0.01  # competitor's fee rate for managing their client's assets
perf_fee_regime = 'v3'
#'v1' is such that we pay client if we do worse than 0
#'v2' perf fee charged so long as beat market
#'v3' perf fee charged if beat market AND > 0

# PERFORMANCE
mkt_perf = 0.12
our_perf = 0.42
comp_perf = 0.20

# EXPENSES
overhead_cost = 0
comp_overhead_cost = 0

# COMPETITIVE EDGE
switch_factor = 0.20  # switch_factor = how much more must the client earn with us than with the competitor for the client to switch over? (represented as a proportion of the amount gained had the client gone with the competitor.  E.g. If the switchfactor was 5%, and client earned $100 investing thru competitor, then for the client to go with us, they would have needed to earn at least an additional $5, for a total gain of $105. If the client earned $102 thru us, that means the client would not switch to us because they would've earned only $2 more, or 2%, which is less than the 5% required.)

# SEPARATE PARAMETERS INTO OURS AND COMPETITORS
our_params = FundProfile('DAVID', client_principal, num_clients, perf_cut, aum_rate, mkt_perf, our_perf, overhead_cost, perf_fee_regime)
comp_params = FundProfile('COMPETITOR', client_principal, comp_num_clients, comp_perf_cut, comp_aum_rate, mkt_perf, comp_perf, comp_overhead_cost, perf_fee_regime)
mkt_params = FundProfile('MARKET', client_principal, comp_num_clients, 0, 0, mkt_perf, mkt_perf, 0, perf_fee_regime)


'''QUESTION: IF THE SWITCHFACTOR IS X, HOW MUCH BETTER MUST I DO THAN COMPETITOR?'''
pd.set_option("display.max_rows", None, "display.max_columns", None)
comp_edge_needed(switch_factor, our_params, comp_params, mkt_params)


'''IF WE ARE GOING WITH AN AUM + PERF MODEL, HOW MUCH OF A LOSS PER YEAR MUST WE PLAN FOR, WHAT CLIENT MONTHLY FEE DOES THAT TRANSLATE INTO, AND WHAT PROPORTION OF THE CLIENT PRINCIPAL IS THAT?'''

# worse_case_scenario_loss = np.min(list_of_perf_fees)
# per_month_cost = worse_case_scenario_loss / 12
# pct_client_principal = per_month_cost / client_principal
# max_edge_rate = np.max(range_edge_rates)

'''
GRAPHING:

QUESTIONS TO ANSWER:
How much better must my fund perform to win the client over from the competitor?
If switch_factor is constant, what is the edge_rate as a function of competitor's performance rate?  (x-axis = comp_perf, y-axis = edge_rate, or our_perf [edge_rate + comp_perf])
'''
# SET PARAMS
num_datapoints_x = 100
start_xval = -1
end_xval = 1
num_datapoints_y = 100
start_yval = -1
end_yval = 1
#graph_edgerate(num_datapoints_x, start_xval, end_xval, switch_factor, our_params, comp_params, perf_fee_regime)
#graph_edgerate3d(num_datapoints_x, start_xval, end_xval, num_datapoints_y, start_yval, end_yval, switch_factor, our_params, comp_params, perf_fee_regime)
