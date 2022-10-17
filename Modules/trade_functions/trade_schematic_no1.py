# for each investment period I, where s = start date, e = end date
# run strat S on date s, return portfolio P, where P_j is the strat portfolio for period I_j
# invest A = (C / size of P) on s date, where C is the amount of cash available to invest.
# at e, run strat S on date e again, return portfolio P_next
# determine what stocks need to go, what stocks stay, and what stocks need to be added
    # get list of stocks in P but not in P_next (P_unique). remove these
    # get list of stocks in common with P and P_next (P_common). keep these.
    # get list of stocks in P_next not in P (P_next_unique). add these.
# exit all positions of P_unique. C += total cash from sale
# calculate investment amount A_next
    # A_next = total account value (TAV) / size of P_next
    # although this will be always changing we should stick to a fixed number.
# execute sales in P_common
    # for t in P_common:
        # calculate investment amount A_next
            # A_next = total account value (TAV) / size of P_next
        # adjust
        # if t_value > A_next, sell (t_value - A_next) worth of shares.
            # C += (t_value - A_next)
        # else:
            # add t to list of P_common stocks needed to increase stake (P_common_buy)
        # add t to list of indicating stocks that are currently in new portfolio (P_fulfilled)
# at this point all sales that needed to occur, occurred.
# Purchase shares in P_common_buy
    # for t in P_common_buy:
        # calculate A_next
            # A_next = total account value (TAV) / size of P_next
        # if t_value < A_next, buy (A_next - t_value) worth of shares.
            # C -= (A_next - t_value)
# purchase shares in P_next_unique
    # calculate A_next
        # A_next = C / size of P_next_unique
    # for t in P_next_unique:
        # buy A_next worth of shares in t
